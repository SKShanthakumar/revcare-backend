from datetime import date, time
import traceback
from sqlalchemy import text, select, insert, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.database import Base, engine
from app.database.dependencies import get_postgres_db
from app.models import (
    Role, Permission, Admin, Mechanic, Customer, User,
    FuelType, Manufacturer, CarClass, Car, Area, Address,
    ServiceCategory, Service, PriceChart, service_fuel_types,
    Status, AssignmentType, Timeslot, PaymentMethod,
    NotificationCategory
    )
from .scopes import get_all_scopes, get_admin_scopes, get_mechanic_scopes, get_customer_scopes
from app.auth import hashing
from app.schemas import CustomerCreate, AdminCreate, MechanicCreate
from app.services.user import create_user
from .seed_data import CHENNAI_AREAS, SERVICES_DATA, SERVICE_FUEL_TYPES_DATA, PRICE_CHART_DATA, ALL_STATUSES

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
    """
    Create database triggers and sequences for auto-generating user IDs.
    
    Creates triggers for customers (CST), admins (ADM), and mechanics (MEC)
    to automatically generate unique IDs with proper formatting.
    
    Args:
        db: Async database session
    """
    try:
        await db.execute(text(unique_id_trigger_script))
        await db.commit()
        print("Custom id generation triggers verified/created successfully!")
    except Exception as e:
        await db.rollback()
        print(f"Skipping trigger setup: {e}")

async def init_delete_triggers(db: Session):
    """
    Create database triggers for cascading user deletion.
    
    Creates triggers that automatically delete user records from the users table
    when corresponding customer, admin, or mechanic records are deleted.
    
    Args:
        db: Async database session
    """
    try:
        await db.execute(text(delete_users_trigger_script))
        await db.commit()
        print("Delete user triggers verified/created successfully!")
    except Exception as e:
        await db.rollback()
        print(f"Skipping delete trigger setup: {e}")

async def seed_rbac(db: Session):
    """
    Seed role-based access control (RBAC) data.
    
    Seeds user roles (admin, mechanic, customer), permissions, and
    role-permission relationships. Only seeds if data doesn't already exist.
    
    Args:
        db: Async database session
    """
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

        else:
            print("Permissions already exist, skipping seeding.")
    
    except Exception as e:
        await db.rollback()
        print(f"Error seeding RBAC data: {e}")
        traceback.print_exc()

async def seed_users(db: Session):
    """
    Seed initial user accounts for testing.
    
    Creates sample admin, customer, and mechanic accounts if no users exist.
    Includes: Admin01, two customers (Surya, Rahul), and one mechanic (Arunachalam).
    
    Args:
        db: Async database session
    """
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
                password='Sk18102004.',
                service_category_ids=[1,2,4,5,6,8,9]
            )

            await create_user(db, admin, Admin)
            await create_user(db, customer1, Customer)
            await create_user(db, customer2, Customer)
            await create_user(db, mechanic, Mechanic)

            print("Users seeded successfully!")

    except Exception as e:
        print(f"Error seeding User data: {e}")

async def seed_addresses(db: Session):
    """
    Seed areas and customer addresses.
    
    Seeds Chennai areas with pincodes and creates sample addresses for
    existing customers. Only seeds if data doesn't already exist.
    
    Args:
        db: Async database session
    """
    try:
        # Seed Areas
        result = await db.execute(select(func.count()).select_from(Area))
        area_count = result.scalar()

        if area_count == 0:
            areas = [Area(name=area[0], pincode=area[1]) for area in CHENNAI_AREAS]
            db.add_all(areas)
            await db.commit()
            print(f"Seeded {len(areas)} areas successfully!")
        else:
            print("Areas already exist, skipping seeding.")


        # Insert only if no addresses exist
        result = await db.execute(select(func.count()).select_from(Address))
        address_count = result.scalar()

        if address_count == 0:
            # Fetch two customers (Surya & Rahul)
            result = await db.execute(
                select(Customer).where(Customer.email.in_(["surya@gmail.com", "rahul@gmail.com"]))
            )
            customers = result.scalars().all()

            if not customers:
                print("No customers found. Please seed users first.")
                return

            # Fetch two random areas to assign addresses
            result = await db.execute(select(Area).limit(2))
            areas = result.scalars().all()

            if len(areas) < 2:
                print("Not enough areas to assign addresses.")
                return

            # Create sample addresses
            addresses = [
                Address(
                    customer_id=str(customers[0].id),
                    label="Home",
                    line1="23, Rajiv Gandhi Street",
                    line2="Near Velachery Railway Station",
                    area_id=areas[0].id,
                ),
                Address(
                    customer_id=str(customers[1].id),
                    label="Home",
                    line1="17, Anna Salai",
                    line2="Opposite Express Avenue",
                    area_id=areas[1].id,
                )
            ]
            db.add_all(addresses)
            await db.commit()
            print("Addresses seeded successfully!")
        else:
            print("Addresses already exist, skipping seeding.")

    except Exception as e:
        await db.rollback()
        print(f"Error seeding address data: {e}")

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

async def seed_service_categories(db: Session):
    """
    Seed service categories.
    
    Creates all service categories (Service Packages, Engine Services, Brake Services, etc.)
    if they don't already exist in the database.
    
    Args:
        db: Async database session
    """
    try:
        # Check if service categories already exist
        result = await db.execute(select(func.count()).select_from(ServiceCategory))
        category_count = result.scalar()

        if category_count == 0:
            categories = [
                ServiceCategory(
                    name="Service Packages",
                    description="Pre-designed bundles for hassle-free and complete car care."
                ),
                ServiceCategory(
                    name="Engine Services",
                    description="Comprehensive maintenance to ensure smooth and efficient engine performance."
                ),
                ServiceCategory(
                    name="Brake Services",
                    description="Specialized care to maintain reliable and safe braking performance."
                ),
                ServiceCategory(
                    name="Transmission & Clutch",
                    description="Services to keep shifting smooth and power delivery consistent."
                ),
                ServiceCategory(
                    name="Suspension & Steering",
                    description="Focused care for driving comfort, handling, and long-term stability."
                ),
                ServiceCategory(
                    name="Electrical & Battery",
                    description="Diagnostics and repairs for reliable power and electronic systems."
                ),
                ServiceCategory(
                    name="Air Conditioning & Heating",
                    description="Cooling and heating system services for year-round driving comfort."
                ),
                ServiceCategory(
                    name="Tyres & Wheels",
                    description="Complete tyre and wheel care for safety, balance, and longer tyre life."
                ),
                ServiceCategory(
                    name="Body & Paint Work",
                    description="Cosmetic and structural repairs to restore your vehicle’s look and finish."
                ),
                ServiceCategory(
                    name="Washing & Detailing",
                    description="Thorough cleaning and detailing services for a fresh, polished appearance."
                ),
                ServiceCategory(
                    name="Accessories & Add-Ons",
                    description="Enhancements and installations to upgrade your car’s style and functionality."
                ),
                ServiceCategory(
                    name="Hybrid & EV Services",
                    description="Specialized maintenance and diagnostics for hybrid and electric vehicle systems."
                ),
            ]

            db.add_all(categories)
            await db.commit()
            print("Service categories seeded successfully!")

        else:
            print("Service categories already exist, skipping seeding.")

    except Exception as e:
        await db.rollback()
        print(f"Error seeding service categories: {e}")

async def seed_service_fuel_types(db: Session):
    """Seed the many-to-many relationship between services and fuel types"""
    try:
        # Check if service_fuel_types already exist
        result = await db.execute(select(func.count()).select_from(service_fuel_types))
        count = result.scalar()
        
        if count == 0:
            # Prepare bulk insert data
            fuel_type_mappings = []
            for service_id, fuel_type_ids in SERVICE_FUEL_TYPES_DATA.items():
                for fuel_type_id in fuel_type_ids:
                    fuel_type_mappings.append({
                        "service_id": service_id,
                        "fuel_type_id": fuel_type_id
                    })
            
            # Bulk insert all mappings
            await db.execute(insert(service_fuel_types), fuel_type_mappings)
            await db.commit()
            print(f"Service-fuel-type seeded successfully!")
        else:
            print("Service-fuel type relationships already exist, skipping seeding.")
            
    except Exception as e:
        await db.rollback()
        print(f"Error seeding service-fuel types: {e}")
        raise

async def seed_price_chart(db: Session):
    """Seed the price chart for all services across all car classes"""
    try:
        # Check if price_chart already exists
        result = await db.execute(select(func.count()).select_from(PriceChart))
        count = result.scalar()
        
        if count == 0:
            # Prepare bulk insert data 
            price_entries = []
            for service_price in PRICE_CHART_DATA:
                service_id = service_price["service_id"]
                prices = service_price["prices"]
                
                for car_class_id, price in prices.items():
                    price_entries.append({
                        "service_id": service_id,
                        "car_class_id": car_class_id,
                        "price": price
                    })
            
            # Bulk insert all price entries
            price_objects = [
                PriceChart(
                    service_id=entry["service_id"],
                    car_class_id=entry["car_class_id"],
                    price=entry["price"]
                )
                for entry in price_entries
            ]
            
            db.add_all(price_objects)
            await db.commit()
            print(f"Price chart seeded successfully!")
        else:
            print("Price chart already exists, skipping seeding.")
            
    except Exception as e:
        await db.rollback()
        print(f"Error seeding price chart: {e}")
        raise

async def seed_services(db: Session):
    """
    Seed service records.
    
    Creates all service records from SERVICES_DATA if they don't already exist.
    Services include Basic Service, Oil Change, Brake Pad Replacement, etc.
    
    Args:
        db: Async database session
    """
    try:
        # Check if services already exist
        result = await db.execute(select(func.count()).select_from(Service))
        service_count = result.scalar()
        
        if service_count == 0:
            # Create Service objects from the data
            services = []
            for service_data in SERVICES_DATA:
                service = Service(
                    title=service_data["title"],
                    description=service_data["description"],
                    category_id=service_data["category_id"],
                    works=service_data["works"],
                    warranty_kms=service_data["warranty_kms"],
                    warranty_months=service_data["warranty_months"],
                    time_hrs=service_data["time_hrs"],
                    difficulty=service_data["difficulty"],
                    images=service_data["images"]
                )
                services.append(service)
            
            db.add_all(services)
            await db.commit()
            print(f"Services seeded successfully!")
        else:
            print("Services already exist, skipping seeding.")
            
    except Exception as e:
        await db.rollback()
        print(f"Error seeding services: {e}")
        raise

async def seed_all_service_data(db: Session):
    """Master function to seed all service-related data in correct order"""
    print("Starting service data seeding...")
    
    # Then seed services
    await seed_services(db)
    
    # Then seed service-fuel type relationships
    await seed_service_fuel_types(db)
    
    # Finally seed price chart
    await seed_price_chart(db)
    
    print("All service data seeded successfully!")

async def seed_statuses(db: Session):
    """Seed all required statuses for bookings workflow"""
    try:
        result = await db.execute(select(Status))
        status_objs = result.scalars().all()
        
        if len(status_objs) < len(ALL_STATUSES):
            existing_statuses = { status.name for status in status_objs }
            statuses = [Status(name=status) for status in ALL_STATUSES if status not in existing_statuses]
            
            db.add_all(statuses)
            await db.commit()
            print(f"Statuses seeded successfully!")
        else:
            print("Statuses already exist, skipping seeding.")
            
    except Exception as e:
        await db.rollback()
        print(f"Error seeding status data: {e}")

async def seed_assignment_types(db: Session):
    """Seed all required assignment types for mechanic assignments"""
    try:
        result = await db.execute(select(func.count()).select_from(AssignmentType))
        type_count = result.scalar()
        
        if type_count == 0:
            assignment_types = [
                AssignmentType(name="pickup"),
                AssignmentType(name="drop"),
                AssignmentType(name="service"),
                AssignmentType(name="analysis"),
            ]
            
            db.add_all(assignment_types)
            await db.commit()
            print(f"Assignment types seeded successfully!")
        else:
            print("Assignment types already exist, skipping seeding.")
            
    except Exception as e:
        await db.rollback()
        print(f"Error seeding assignment type data: {e}")

async def seed_timeslots(db: Session):
    """Seed default timeslots for pickup and drop scheduling"""
    try:
        result = await db.execute(select(func.count()).select_from(Timeslot))
        slot_count = result.scalar()
        
        if slot_count == 0:
            timeslots = [
                Timeslot(name="Morning", start_time=time(8, 0), end_time=time(12, 0)),
                Timeslot(name="Afternoon", start_time=time(13, 0), end_time=time(16, 0)),
                Timeslot(name="Evening", start_time=time(16, 0), end_time=time(19, 0)),
                Timeslot(name="Night", start_time=time(19, 0), end_time=time(22, 0)),
            ]
            
            db.add_all(timeslots)
            await db.commit()
            print(f"Timeslots seeded successfully!")
        else:
            print("Timeslots already exist, skipping seeding.")
            
    except Exception as e:
        await db.rollback()
        print(f"Error seeding timeslot data: {e}")

async def seed_booking_data(db: Session):
    """Master function to seed all booking-related data"""
    print("\nStarting booking data seeding...")
    
    await seed_statuses(db)
    await seed_assignment_types(db)
    await seed_timeslots(db)
    
    print("All booking data seeded successfully!")

async def seed_payment_methods(db: Session):
    """Seed payment methods online / offline"""
    try:
        result = await db.execute(select(func.count()).select_from(PaymentMethod))
        count = result.scalar()
        
        if count == 0:
            timeslots = [
                PaymentMethod(name="online"),
                PaymentMethod(name="offline")
            ]
            
            db.add_all(timeslots)
            await db.commit()
            print(f"Payment methods seeded successfully!")
        else:
            print("Payment methods already exist, skipping seeding.")
            
    except Exception as e:
        await db.rollback()
        print(f"Error seeding timeslot data: {e}")

async def seed_notification_categories(db: Session):
    """Seed notification categories"""
    try:
        result = await db.execute(select(func.count()).select_from(NotificationCategory))
        category_count = result.scalar()
        
        if category_count == 0:
            categories = [
                NotificationCategory(name="Booking Confirmation"),
                NotificationCategory(name="Progress Update"),
                NotificationCategory(name="Invoice"),
                NotificationCategory(name="Query Response"),
            ]
            
            db.add_all(categories)
            await db.commit()
            print(f"Notification categories seeded successfully!")
        else:
            print("Notification categories already exist, skipping seeding.")
            
    except Exception as e:
        await db.rollback()
        print(f"Error seeding notification categories: {e}")


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
            await seed_addresses(db)
            await seed_car_utils(db)
            await seed_service_categories(db)
            await seed_all_service_data(db)
            await seed_booking_data(db)
            await seed_payment_methods(db)
            await seed_notification_categories(db)
            
        finally:
            await db.close()