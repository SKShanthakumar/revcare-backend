from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.auth import hashing
from app.models import Customer, User, Role, Admin, Mechanic
from app.schemas import CustomerCreate, CustomerUpdate, AdminUpdate, AdminCreate, MechanicCreate, MechanicUpdate

def get_all_users(db: Session, model: Customer | Admin | Mechanic):
    return db.query(model).all()

def get_user_by_id(db: Session, user_id: str, model: Customer | Admin | Mechanic):
    user = db.query(model).filter(model.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

def update_user(db: Session, user_id: str, user_data: CustomerUpdate | AdminUpdate | MechanicUpdate, model: Customer | Admin | Mechanic):
    user = db.query(model).filter(model.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    for key, value in user_data.model_dump().items():
        if value is not None:
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

def create_user(db: Session, user: CustomerCreate | AdminCreate | MechanicCreate, model: Customer | Admin | Mechanic):
    phone = user.phone
    hashed_password = hashing.hash_password(user.password)
    model_name = model.__name__.lower()

    # extract user role id
    user_role = db.query(Role).filter(Role.role_name.ilike(model_name)).first()
    if not user_role:
        raise HTTPException(status_code=500, detail="Specified role not found.")
    
    # Create and commit user first
    existing = db.query(User).filter(User.phone == phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this phone number already exists.")
    
    db_user = User(phone=phone, password=hashed_password, role_id=user_role.id)
    db.add(db_user)
    db.commit()

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
            existing = db.query(model).filter(model.email == user.email).first()
            if existing:
                raise HTTPException(status_code=400, detail="User with this email already exists.")
            
            # create user
            db_user = model(name=user.name, phone=user.phone, email=user.email, role_id=user_role.id)
        db.add(db_user)    
        db.commit()
        db.refresh(db_user)
        return db_user
    
    except Exception as e:
        # If user creation fails, rollback and delete the user
        db.rollback()
        db.query(User).filter(User.phone == phone).delete()
        db.commit()
        raise e
    
def delete_user(db: Session, user_id: str, model: Customer | Admin | Mechanic):
    user = db.query(model).filter(model.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user_phone = user.phone
    user = db.query(User).filter(User.phone == user_phone).first()
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully."}