import asyncio
from sqlalchemy import text, select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.database import Base, engine
from app.database.dependencies import get_postgres_db
from app.models import Role, Permission
from .scopes import get_all_scopes, get_admin_scopes, get_mechanic_scopes, get_customer_scopes

unique_id_trigger_script = """
-- ===========================
-- CUSTOMERS
-- ===========================
CREATE SEQUENCE IF NOT EXISTS customer_seq START 1;

CREATE OR REPLACE FUNCTION generate_customer_id()
RETURNS TRIGGER AS $$
BEGIN
  NEW.id := 'CST' || LPAD(nextval('customer_seq')::text, 6, '0');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'customer_id_trigger') THEN
    CREATE TRIGGER customer_id_trigger
    BEFORE INSERT ON customers
    FOR EACH ROW
    EXECUTE FUNCTION generate_customer_id();
  END IF;
END $$;


-- ===========================
-- ADMINS
-- ===========================
CREATE SEQUENCE IF NOT EXISTS admin_seq START 1;

CREATE OR REPLACE FUNCTION generate_admin_id()
RETURNS TRIGGER AS $$
BEGIN
  NEW.id := 'ADM' || LPAD(nextval('admin_seq')::text, 6, '0');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'admin_id_trigger') THEN
    CREATE TRIGGER admin_id_trigger
    BEFORE INSERT ON admins
    FOR EACH ROW
    EXECUTE FUNCTION generate_admin_id();
  END IF;
END $$;


-- ===========================
-- MECHANICS
-- ===========================
CREATE SEQUENCE IF NOT EXISTS mechanic_seq START 1;

CREATE OR REPLACE FUNCTION generate_mechanic_id()
RETURNS TRIGGER AS $$
BEGIN
  NEW.id := 'MEC' || LPAD(nextval('mechanic_seq')::text, 6, '0');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'mechanic_id_trigger') THEN
    CREATE TRIGGER mechanic_id_trigger
    BEFORE INSERT ON mechanics
    FOR EACH ROW
    EXECUTE FUNCTION generate_mechanic_id();
  END IF;
END $$;
"""

delete_users_trigger_script = """
-- Create or replace the trigger function
CREATE OR REPLACE FUNCTION delete_user_on_child_delete()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM users WHERE phone = OLD.phone;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Conditionally create triggers only if they don't exist
DO $$
BEGIN
    -- Customers trigger
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'trg_delete_user_from_customers'
    ) THEN
        CREATE TRIGGER trg_delete_user_from_customers
        AFTER DELETE ON customers
        FOR EACH ROW
        EXECUTE FUNCTION delete_user_on_child_delete();
    END IF;

    -- Admins trigger
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'trg_delete_user_from_admins'
    ) THEN
        CREATE TRIGGER trg_delete_user_from_admins
        AFTER DELETE ON admins
        FOR EACH ROW
        EXECUTE FUNCTION delete_user_on_child_delete();
    END IF;

    -- Mechanics trigger
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'trg_delete_user_from_mechanics'
    ) THEN
        CREATE TRIGGER trg_delete_user_from_mechanics
        AFTER DELETE ON mechanics
        FOR EACH ROW
        EXECUTE FUNCTION delete_user_on_child_delete();
    END IF;
END $$;
"""

async def init_custom_triggers(db: Session):
    """Create triggers and sequences"""
    try:
        await db.execute(text(unique_id_trigger_script))
        await db.commit()
        print("Custom id generation triggers verified/created successfully!")
    except Exception as e:
        await db.rollback()
        print(f"Skipping trigger setup: {e}")

async def init_delete_triggers(db: Session):
    """Create delete triggers"""
    try:
        await db.execute(text(delete_users_trigger_script))
        await db.commit()
        print("Delete user triggers verified/created successfully!")
    except Exception as e:
        await db.rollback()
        print(f"Skipping delete trigger setup: {e}")

async def seed_rbac(db: Session):
    """Seed user roles (only if not already seeded)"""
    try:
        result = await db.execute(select(func.count()).select_from(Role))
        existing_roles = result.scalar()
        if existing_roles == 0:
            db.add_all([
                Role(role_name="admin"),
                Role(role_name="mechanic"),
                Role(role_name="customer"),
            ])
            await db.commit()
            print("Roles seeded successfully!")
        else:
            print("Roles already exist, skipping seeding.")

        # Refresh to get IDs after potential commit
        result = await db.execute(select(Role).options(selectinload(Role.permissions)))
        roles = {r.role_name: r for r in result.scalars().all()}

        # Seed permissions (if not already)
        result = await db.execute(select(func.count()).select_from(Permission))
        existing_permissions = result.scalar_one()
        if existing_permissions == 0:
            permissions_data = get_all_scopes()
            permissions = [Permission(permission=p) for p in permissions_data]
            db.add_all(permissions)
            await db.commit()
            print("Permissions seeded successfully!")

        else:
            print("Permissions already exist, skipping seeding.")

        # Refresh permission objects
        result = await db.execute(select(Permission))
        all_permissions = {p.permission: p for p in result.scalars().all()}
        # Group permissions by role
        admin_perm_names = get_admin_scopes()
        mechanic_perm_names = get_mechanic_scopes()
        customer_perm_names = get_customer_scopes()

        admin_permissions = [all_permissions[name] for name in admin_perm_names]
        mechanic_permissions = [all_permissions[name] for name in mechanic_perm_names]
        customer_permissions = [all_permissions[name] for name in customer_perm_names]
        
        # optionally clear existing relationships
        for role in roles.values():
            role.permissions.clear()
            
        roles["admin"].permissions = admin_permissions
        roles["mechanic"].permissions = mechanic_permissions
        roles["customer"].permissions = customer_permissions

        await db.commit()
        print("Role-permission relationships seeded successfully!")

    except Exception as e:
        await db.rollback()
        print(f"Error seeding RBAC data: {e}")


async def run_seed():
    """Run all startup DB seeding logic"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for db in get_postgres_db():
        try:
            await init_custom_triggers(db)
            await init_delete_triggers(db)
            await seed_rbac(db)
        finally:
            await db.close()