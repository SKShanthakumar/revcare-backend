from datetime import date
from sqlalchemy import text, select, func, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.database import Base, engine
from app.database.dependencies import get_postgres_db
from app.models import Role, Permission, Admin, Mechanic, Customer, User, FuelType, Manufacturer, CarClass, Car
from .scopes import get_all_scopes, get_admin_scopes, get_mechanic_scopes, get_customer_scopes
from app.auth import hashing
from app.schemas import CustomerCreate, AdminCreate, MechanicCreate
from app.services.user import create_user

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
        result = await db.execute(select(Permission))
        existing_permissions = {row.permission for row in result.scalars().all()}

        permissions_data = set(get_all_scopes())

        # Find permissions that are not yet in the database
        new_permissions = permissions_data - existing_permissions

        if new_permissions:
            permissions = [Permission(permission=p) for p in new_permissions]
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

async def seed_users(db: Session):
    try:
        result = await db.execute(select(func.count()).select_from(User))
        user_count = result.scalar()
        if user_count == 0:
            admin = AdminCreate(
                name="Admin01",
                phone=9841385379,
                email="admin01@gmail.com",
                password="Sk18102004."
            )

            customer1 = CustomerCreate(
                name="Surya",
                phone=7904593204,
                email="surya@gmail.com",
                password="Sk18102004."
            )

            customer2 = CustomerCreate(
                name="Rahul",
                phone=7904593205,
                email="rahul@gmail.com",
                password="Sk18102004."
            )

            mechanic = MechanicCreate(
                name="Arunachalam",
                phone="6374159500",
                dob=date(year=2000, month=12, day=12),
                pickup_drop=False,
                analysis=True,
                password='Sk18102004.'
            )

            await create_user(db, admin, Admin)
            await create_user(db, customer1, Customer)
            await create_user(db, customer2, Customer)
            await create_user(db, mechanic, Mechanic)

            print("Users seeded successfully!")

    except Exception as e:
        print(f"Error seeding User data: {e}")

async def seed_car_utils(db: Session):
    """Seed car-related utility tables (fuel types, manufacturers, car classes, and sample cars)"""
    try:
        # Seed Fuel Types
        result = await db.execute(select(func.count()).select_from(FuelType))
        fuel_count = result.scalar()
        if fuel_count == 0:
            fuel_types = [
                FuelType(fuel_name="Petrol"),
                FuelType(fuel_name="Diesel"),
                FuelType(fuel_name="Electric"),
                FuelType(fuel_name="Hybrid"),
                FuelType(fuel_name="CNG"),
            ]
            db.add_all(fuel_types)
            await db.commit()
            print("Fuel types seeded successfully!")
        else:
            print("Fuel types already exist, skipping seeding.")

        # Seed Manufacturers
        result = await db.execute(select(func.count()).select_from(Manufacturer))
        manufacturer_count = result.scalar()
        if manufacturer_count == 0:
            manufacturers = [
                Manufacturer(name="Maruti Suzuki"),
                Manufacturer(name="Hyundai"),
                Manufacturer(name="Tata"),
                Manufacturer(name="Mahindra"),
                Manufacturer(name="Honda"),
                Manufacturer(name="Toyota"),
                Manufacturer(name="Kia"),
                Manufacturer(name="MG"),
                Manufacturer(name="Volkswagen"),
                Manufacturer(name="Skoda"),
                Manufacturer(name="Renault"),
                Manufacturer(name="Nissan"),
                Manufacturer(name="Ford"),
                Manufacturer(name="Jeep"),
                Manufacturer(name="Mercedes-Benz"),
                Manufacturer(name="BMW"),
                Manufacturer(name="Audi"),
                Manufacturer(name="Volvo"),
                Manufacturer(name="Lexus"),
                Manufacturer(name="Porsche"),
                Manufacturer(name="Jaguar"),
                Manufacturer(name="Land Rover"),
                Manufacturer(name="BYD"),
                Manufacturer(name="Citroën"),
                Manufacturer(name="Isuzu"),
                Manufacturer(name="Fiat"),
            ]
            db.add_all(manufacturers)
            await db.commit()
            print("Manufacturers seeded successfully!")
        else:
            print("Manufacturers already exist, skipping seeding.")

        # Seed Car Classes
        result = await db.execute(select(func.count()).select_from(CarClass))
        class_count = result.scalar()
        if class_count == 0:
            car_classes = [
                CarClass(class_="Basic Hatchback"),
                CarClass(class_="Premium Hatchback"),
                CarClass(class_="Luxury Hatchback"),

                CarClass(class_="Basic Sedan"),
                CarClass(class_="Premium Sedan"),
                CarClass(class_="Luxury Sedan"),

                CarClass(class_="Basic SUV"),
                CarClass(class_="Premium SUV"),
                CarClass(class_="Luxury SUV"),

                CarClass(class_="Basic MPV"),
                CarClass(class_="Premium MPV"),
                CarClass(class_="Luxury MPV"),

                CarClass(class_="Premium Coupe"),
                CarClass(class_="Luxury Coupe"),

                CarClass(class_="Premium Convertible"),
                CarClass(class_="Luxury Convertible"),

                CarClass(class_="Basic Crossover"),
                CarClass(class_="Premium Crossover"),
                CarClass(class_="Luxury Crossover"),

                CarClass(class_="Basic Pickup Truck"),
                CarClass(class_="Premium Pickup Truck"),
            ]
            db.add_all(car_classes)
            await db.commit()
            print("Car classes seeded successfully!")
        else:
            print("Car classes already exist, skipping seeding.")

        # Refresh to get IDs after commits
        result = await db.execute(select(FuelType))
        fuel_types_dict = {ft.fuel_name: ft for ft in result.scalars().all()}
        
        result = await db.execute(select(Manufacturer))
        manufacturers_dict = {m.name: m for m in result.scalars().all()}
        
        result = await db.execute(select(CarClass))
        car_classes_dict = {cc.class_: cc for cc in result.scalars().all()}

        # Seed Sample Cars
        result = await db.execute(select(func.count()).select_from(Car))
        car_count = result.scalar()
        if car_count == 0:
            cars = [
                Car(
                    model="Swift",
                    manufacturer_id=manufacturers_dict["Maruti Suzuki"].id,
                    fuel_type_id=fuel_types_dict["Petrol"].id,
                    car_class_id=car_classes_dict["Basic Hatchback"].id,
                    year=2024,
                    img="swift.jpg"
                ),
                Car(
                    model="Creta",
                    manufacturer_id=manufacturers_dict["Hyundai"].id,
                    fuel_type_id=fuel_types_dict["Diesel"].id,
                    car_class_id=car_classes_dict["Premium SUV"].id,
                    year=2024,
                    img="creta.jpg"
                ),
                Car(
                    model="Nexon EV",
                    manufacturer_id=manufacturers_dict["Tata"].id,
                    fuel_type_id=fuel_types_dict["Electric"].id,
                    car_class_id=car_classes_dict["Premium SUV"].id,
                    year=2023,
                    img="nexon_ev.jpg"
                ),
                Car(
                    model="Fortuner",
                    manufacturer_id=manufacturers_dict["Toyota"].id,
                    fuel_type_id=fuel_types_dict["Diesel"].id,
                    car_class_id=car_classes_dict["Premium SUV"].id,
                    year=2024,
                    img="fortuner.jpg"
                ),
                Car(
                    model="City",
                    manufacturer_id=manufacturers_dict["Honda"].id,
                    fuel_type_id=fuel_types_dict["Petrol"].id,
                    car_class_id=car_classes_dict["Premium Sedan"].id,
                    year=2024,
                    img="city.jpg"
                ),
            ]
            db.add_all(cars)
            await db.commit()
            print("Sample cars seeded successfully!")
        else:
            print("Cars already exist, skipping seeding.")

    except Exception as e:
        await db.rollback()
        print(f"Error seeding Car utils data: {e}")


async def run_seed():
    """Run all startup DB seeding logic"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for db in get_postgres_db():
        try:
            await init_custom_triggers(db)
            await init_delete_triggers(db)
            await seed_rbac(db)
            await seed_users(db)
            await seed_car_utils(db)

        finally:
            await db.close()