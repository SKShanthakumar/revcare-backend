from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession as Session
from app.auth import hashing
from app.models import Customer, User, Role, Admin, Mechanic
from app.schemas import CustomerCreate, AdminCreate, MechanicCreate

async def create_user(db: Session, user: CustomerCreate | AdminCreate | MechanicCreate, model: Customer | Admin | Mechanic):
    phone = user.phone
    hashed_password = hashing.hash_password(user.password)
    model_name = model.__name__.lower()

    # extract user role id
    result = await db.execute(select(Role).where(Role.role_name.ilike(model_name)))
    user_role = result.scalar_one_or_none()
    if not user_role:
        raise HTTPException(status_code=500, detail="Specified role not found.")
    
    # Create and commit user first
    result = await db.execute(select(User).where(User.phone == phone))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="User with this phone number already exists.")
    
    db_user = User(phone=phone, password=hashed_password, role_id=user_role.id)
    db.add(db_user)
    await db.commit()

    try:
        if model_name == "mechanic":
            db_user = model(
                name=user.name,
                phone=phone,
                dob=user.dob,
                pickup_drop=user.pickup_drop,
                analysis=user.analysis,
                role_id=user_role.id
            )
        else:
            result = await db.execute(select(model).where(model.email == user.email))
            existing = result.scalar_one_or_none()
            if existing:
                raise HTTPException(status_code=400, detail="User with this email already exists.")
            
            # create user
            db_user = model(name=user.name, phone=user.phone, email=user.email, role_id=user_role.id)
        db.add(db_user)    
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    except Exception as e:
        # If user creation fails, rollback and delete the user
        await db.rollback()
        await db.execute(delete(User).where(User.phone == phone))
        await db.commit()
        raise e
    