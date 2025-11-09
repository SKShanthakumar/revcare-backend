from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.strategy_options import _AbstractLoad
from typing import Dict, Any, Optional, List

async def get_all_records(
        db: Session,
        model: Any,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[InstrumentedAttribute] = None,
        desc: bool = False,
        options: Optional[List[_AbstractLoad]] = None,
    ):
    """
    Retrieve all records from a model with optional filtering, pagination, and ordering.
    
    Args:
        db: Async database session
        model: SQLAlchemy model class
        filters: Optional dictionary of field:value pairs to filter by
        limit: Optional maximum number of records to return
        offset: Optional number of records to skip
        order_by: Optional model attribute to order by
        desc: If True, order descending; if False, order ascending
        options: Optional list of SQLAlchemy loading options (selectinload, joinedload, etc.)
        
    Returns:
        list: List of model instances matching the criteria
    """
    query = select(model)

    # Apply ORM options like selectinload, joinedload, etc.
    if options:
        query = query.options(*options)

    # Apply filters dynamically
    if filters:
        for field_name, value in filters.items():
            if hasattr(model, field_name):
                field = getattr(model, field_name)
                if isinstance(value, (list, tuple, set)):
                    query = query.where(field.in_(value))
                else:
                    query = query.where(field == value)

    # Apply sorting
    if order_by is not None:
        query = query.order_by(order_by.desc() if desc else order_by.asc())

    # Apply pagination
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    result = await db.execute(query)
    return result.scalars().all()

async def get_one_record(
    db: Session,
    model: Any,
    filters: Optional[Dict[str, Any]] = None,
    options: Optional[List[_AbstractLoad]] = None,
) -> Optional[Any]:
    """
    Retrieve a single record from a model with optional filtering.
    
    Args:
        db: Async database session
        model: SQLAlchemy model class
        filters: Optional dictionary of field:value pairs to filter by
        options: Optional list of SQLAlchemy loading options (selectinload, joinedload, etc.)
        
    Returns:
        Optional[Any]: Model instance if found, None otherwise
    """
    query = select(model)

    if options:
        query = query.options(*options)

    if filters:
        for field_name, value in filters.items():
            if hasattr(model, field_name):
                query = query.where(getattr(model, field_name) == value)

    result = await db.execute(query)
    return result.scalars().first()

async def get_record_by_primary_key(db: Session, pk, model):
    """
    Retrieve a record by its primary key.
    
    Args:
        db: Async database session
        pk: Primary key value
        model: SQLAlchemy model class
        
    Returns:
        Any: Model instance
        
    Raises:
        HTTPException: 404 if record is not found
    """
    record = await db.get(model, pk)
    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found.")
    return record

async def create_record(db: Session, data: dict, model):
    """
    Create a new record in the database.
    
    Args:
        db: Async database session
        data: Dictionary of field:value pairs for the new record
        model: SQLAlchemy model class
        
    Returns:
        Any: Created model instance
        
    Raises:
        HTTPException: 400 if there's an integrity error (e.g., invalid foreign key)
    """
    try:
        record = model(**data)
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid foreign key reference")

async def update_record_by_primary_key(db: Session, id: str, new_data: dict, model):
    """
    Update a record by its primary key.
    
    Args:
        db: Async database session
        id: Primary key value
        new_data: Dictionary of field:value pairs to update
        model: SQLAlchemy model class
        
    Returns:
        Any: Updated model instance
        
    Raises:
        HTTPException: 404 if record is not found
    """
    record = await db.get(model, id)
    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found.")
    
    for key, value in new_data.items():
        if hasattr(record, key):  # avoid attribute errors
            setattr(record, key, value)
    
    await db.commit()
    await db.refresh(record)
    return record

async def delete_record_by_primary_key(db: Session, pk, model):
    """
    Delete a record by its primary key.
    
    Args:
        db: Async database session
        pk: Primary key value
        model: SQLAlchemy model class
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if record is not found
    """
    record = await db.get(model, pk)
    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found.")

    await db.delete(record)
    await db.commit()

    return {"detail": f"{model.__name__} deleted successfully."}

async def update_record_by_composite_key(db: Session, pk: dict, new_data: dict, model):
    """
    Update a record by its composite primary key.
    
    Args:
        db: Async database session
        pk: Dictionary of primary key fields, e.g. {"user_id": "CST000123", "service_id": 42}
        new_data: Dictionary of field:value pairs to update
        model: SQLAlchemy model class
        
    Returns:
        Any: Updated model instance
        
    Raises:
        HTTPException: 404 if record is not found
    """
    # Build query for composite or single PK
    filters = [getattr(model, key) == value for key, value in pk.items()]
    query = select(model).where(and_(*filters))
    result = await db.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found.")
    
    for key, value in new_data.items():
        if hasattr(record, key):
            setattr(record, key, value)

    await db.commit()
    await db.refresh(record)
    return record


async def delete_record_by_composite_key(db: Session, pk: dict, model):
    """
    Delete a record by its composite primary key.
    
    Args:
        db: Async database session
        pk: Dictionary of primary key fields, e.g. {"user_id": "CST000123", "service_id": 42}
        model: SQLAlchemy model class
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: 404 if record is not found
    """
    filters = [getattr(model, key) == value for key, value in pk.items()]
    query = select(model).where(and_(*filters))
    result = await db.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found.")

    await db.delete(record)
    await db.commit()

    return {"detail": f"{model.__name__} deleted successfully."}
