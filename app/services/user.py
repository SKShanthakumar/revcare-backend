from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.exc import IntegrityError
from app.auth import hashing
from app.models import Customer, User, Role, Admin, Mechanic, ServiceCategory
from app.schemas import CustomerCreate, CustomerUpdate, AdminCreate, MechanicCreate, MechanicUpdate, MechanicUpdateWithForeignData
from app.utilities.data_utils import filter_data_for_model
from app.services import crud

async def create_user(db: Session, user: CustomerCreate | AdminCreate, model: Customer | Admin):
    """
    Create a new user (Customer or Admin) with authentication credentials.
    
    Creates both a User record (for authentication) and a Customer/Admin record
    (for role-specific data) in a single transaction.
    
    Args:
        db: Async database session
        user: Customer or Admin creation schema
        model: Customer or Admin model class
        
    Returns:
        Customer | Admin: Created user instance
        
    Raises:
        HTTPException: 
            - 500 if role is not found
            - 400 if phone or email already exists
            - 400 if there's duplicate or invalid data
    """
    phone = user.phone
    hashed_password = hashing.hash_password(user.password)
    model_name = model.__name__.lower()

    # Get user role
    result = await db.execute(select(Role).where(Role.role_name.ilike(model_name)))
    user_role = result.scalar_one_or_none()
    if not user_role:
        raise HTTPException(status_code=500, detail="Specified role not found.")

    # Check if phone already exists (optional for friendly message)
    result = await db.execute(select(User).where(User.phone == phone))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User with this phone number already exists.")

    # Check if email already exists in Customer/Admin
    result = await db.execute(select(model).where(model.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    # Create both records within one transaction
    db_user = User(phone=phone, password=hashed_password, role_id=user_role.id)
    db.add(db_user)
    await db.flush()

    db_sub_user = model(
        name=user.name,
        phone=user.phone,
        email=user.email,
        role_id=user_role.id
    )
    db.add(db_sub_user)

    try:
        await db.commit()
        await db.refresh(db_sub_user)
        return db_sub_user

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Duplicate or invalid data detected.")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def get_mechanics(db: Session, payload: dict, mechanic_id: str | None):
    """
    Get mechanic(s) information with access control.
    
    If mechanic_id is provided, returns that specific mechanic (with permission check).
    Otherwise, returns all mechanics or just the logged-in mechanic based on role.
    
    Args:
        db: Async database session
        payload: Token payload containing user_id and role
        mechanic_id: Optional mechanic ID to filter by
        
    Returns:
        list: List of Mechanic instances
        
    Raises:
        HTTPException: 403 if mechanic tries to access another mechanic's data
    """
    filters = None
    if mechanic_id is not None:
        if payload.get("role") == 2 and (mechanic_id != payload.get("user_id")):
            raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other mechanics.")
        
        filters = {"id": mechanic_id}
    else:
        user_id = payload.get("user_id")
        if user_id.startswith("MEC"):
            filters = {"id": user_id}

    return await crud.get_all_records(db, Mechanic, filters=filters)


async def create_mechanic(db: Session, user: MechanicCreate):
    """
    Create a new mechanic with authentication credentials and service categories.
    
    Creates both a User record (for authentication) and a Mechanic record
    with associated service categories in a single transaction.
    
    Args:
        db: Async database session
        user: Mechanic creation schema
        
    Returns:
        Mechanic: Created mechanic instance
        
    Raises:
        HTTPException: 
            - 500 if mechanic role is not found
            - 400 if phone already exists
            - 400 if there's duplicate or invalid data
    """
    phone = user.phone
    hashed_password = hashing.hash_password(user.password)

    # Get user role
    result = await db.execute(select(Role).where(Role.role_name.ilike("mechanic")))
    role_object = result.scalar_one_or_none()
    if not role_object:
        raise HTTPException(status_code=500, detail="Mechanic role not found.")
    
    # Check if phone already exists (optional for friendly message)
    result = await db.execute(select(User).where(User.phone == phone))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User with this phone number already exists.")

    # Create record in users table (common for all 3 users)
    db_user = User(phone=phone, password=hashed_password, role_id=role_object.id)
    db.add(db_user)
    await db.flush()

    filtered_data = filter_data_for_model(Mechanic, user.model_dump())
    filtered_data["role_id"] = role_object.id
    db_sub_user = Mechanic(**filtered_data)

    # fetch service category models to establish relationship
    if user.service_category_ids:
        filters = {"id": user.service_category_ids}
        service_category_models = await crud.get_all_records(db, ServiceCategory, filters=filters)
        db_sub_user.service_categories = service_category_models
    db.add(db_sub_user)

    try:
        await db.commit()
        await db.refresh(db_sub_user)
        return db_sub_user

    except IntegrityError as e:
        await db.rollback()
        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=400, detail="Duplicate or invalid data detected.")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    

async def update_mechanic(db: Session, mechanic_id: int, update_schema: MechanicUpdateWithForeignData, payload: dict):
    """
    Update mechanic information including service categories.
    
    Updates basic mechanic fields and/or service category associations.
    Enforces access control - mechanics can only update their own data.
    
    Args:
        db: Async database session
        mechanic_id: ID of mechanic to update
        update_schema: Update schema with mechanic fields and service_category_ids
        payload: Token payload containing user_id and role
        
    Returns:
        Mechanic: Updated mechanic instance
        
    Raises:
        HTTPException: 
            - 403 if mechanic tries to update another mechanic's data
            - 404 if mechanic is not found
            - 400 if there's duplicate or invalid data
    """
    if payload.get("role") == 2 and payload.get("user_id") != mechanic_id:
        raise HTTPException(status_code=403, detail="Operation not permitted.")
    
    mechanic_base_schema = MechanicUpdate(**update_schema.model_dump(exclude_none=True))
    new_data = mechanic_base_schema.model_dump(exclude_none=True)

    mechanic: Mechanic = await crud.get_record_by_primary_key(db, mechanic_id, Mechanic)
    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found")

    flag = False    # to check any db transaction made
    
    if new_data:
        flag = True
        await crud.update_record_by_primary_key(db, mechanic_id, new_data, Mechanic)
    
    if update_schema.service_category_ids is not None:
        flag = True
        if len(update_schema.service_category_ids) > 0:
            filters = {"id": update_schema.service_category_ids}
            service_category_models = await crud.get_all_records(db, ServiceCategory, filters=filters)
            print(service_category_models)
            mechanic.service_categories = service_category_models
        else:
            mechanic.service_categories = []

    if flag:
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Duplicate or invalid data detected.")

    await db.refresh(mechanic)

    return mechanic


async def delete_mechanic(id: str, db: Session, payload: dict):
    """
    Delete a mechanic account.
    
    Enforces access control - mechanics can only delete their own account.
    
    Args:
        id: Mechanic ID to delete
        db: Async database session
        payload: Token payload containing user_id and role
        
    Returns:
        JSONResponse: Success message
        
    Raises:
        HTTPException: 403 if mechanic tries to delete another mechanic's account
    """
    if payload.get("role") == 2 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other mechanics.")
    
    message = await crud.delete_record_by_primary_key(db, id.strip(), Mechanic)
    return JSONResponse(content=message)


async def get_customers(db: Session, payload: dict, customer_id: str | None):
    """
    Get customer(s) information with access control.
    
    If customer_id is provided, returns that specific customer (with permission check).
    Otherwise, returns all customers or just the logged-in customer based on role.
    
    Args:
        db: Async database session
        payload: Token payload containing user_id and role
        customer_id: Optional customer ID to filter by
        
    Returns:
        list: List of Customer instances
        
    Raises:
        HTTPException: 403 if customer tries to access another customer's data
    """
    filters = None
    if customer_id is not None:
        if payload.get("role") == 3 and (customer_id != payload.get("user_id")):
            raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other customers.")
        
        filters = {"id": customer_id}
    else:
        user_id = payload.get("user_id")
        if user_id.startswith("CST"):
            filters = {"id": user_id}

    return await crud.get_all_records(db, Customer, filters=filters)


async def update_customer(id: str, customer_data: CustomerUpdate, db: Session, payload: dict):
    """
    Update customer information.
    
    Enforces access control - customers can only update their own data.
    
    Args:
        id: Customer ID to update
        customer_data: Updated customer data
        db: Async database session
        payload: Token payload containing user_id and role
        
    Returns:
        Customer: Updated customer instance
        
    Raises:
        HTTPException: 403 if customer tries to update another customer's data
    """
    if payload.get("role") == 3 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other customers.")
    
    return await crud.update_record_by_primary_key(db, id.strip(), customer_data.model_dump(exclude_none=True), Customer)


async def delete_customer(id: str, db: Session, payload: dict):
    """
    Delete a customer account.
    
    Enforces access control - customers can only delete their own account.
    
    Args:
        id: Customer ID to delete
        db: Async database session
        payload: Token payload containing user_id and role
        
    Returns:
        JSONResponse: Success message
        
    Raises:
        HTTPException: 403 if customer tries to delete another customer's account
    """
    if payload.get("role") == 3 and payload.get("user_id") != id:
        raise HTTPException(status_code=403, detail="Operation not permitted. Trying to access data of other customers.")
    
    message = await crud.delete_record_by_primary_key(db, id.strip(), Customer)
    return JSONResponse(content=message)
