from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.auth import hashing
from app.models import Customer, User, Role, Admin
from app.schemas import CustomerCreate, CustomerUpdate, AdminUpdate, AdminCreate

def get_all_users(db: Session, model: Customer | Admin):
    return db.query(model).all()

def get_user_by_id(db: Session, user_id: str, model: Customer | Admin):
    user = db.query(model).filter(model.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

def update_user(db: Session, user_id: str, user_data: CustomerUpdate | AdminUpdate, model: Customer | Admin):
    user = db.query(model).filter(model.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    for key, value in user_data.model_dump().items():
        if value is not None:
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

def create_user(db: Session, user: CustomerCreate | AdminCreate, model: Customer | Admin):
    phone = str(user.phone)
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
        existing = db.query(model).filter(model.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="User with this email already exists.")
        
        # create user
        db_user = model(name=user.name, phone=user.phone, email=user.email)
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
    
def delete_user(db: Session, user_id: str, model: Customer | Admin):
    user = db.query(model).filter(model.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully."}