from sqlalchemy import text
from app.database import Base, engine
from app.database.dependencies import get_postgres_db
from app.models import Role


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

def init_custom_triggers(db):
    """Create triggers and sequences"""
    try:
        db.execute(text(unique_id_trigger_script))
        db.commit()
        print("Custom triggers verified/created successfully!")
    except Exception as e:
        db.rollback()
        print(f"Skipping trigger setup: {e}")


def seed_roles(db):
    """Seed user roles (only if not already seeded)"""
    try:
        existing_roles = db.query(Role).count()
        if existing_roles == 0:
            roles_data = [
                {"role_name": "admin"},
                {"role_name": "mechanic"},
                {"role_name": "customer"},
            ]
            db.bulk_insert_mappings(Role, roles_data)
            db.commit()
            print("Roles seeded successfully!")
        else:
            print("Roles already exist, skipping seeding.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding roles: {e}")


def seed_database():
    """Initialize database with triggers and base data"""
    # Create all tables (no drop!)
    Base.metadata.create_all(bind=engine)

    # Manually obtain DB session
    db = next(get_postgres_db())

    try:
        init_custom_triggers(db)
        seed_roles(db)
    finally:
        db.close()
