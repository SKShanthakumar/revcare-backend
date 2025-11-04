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
    record = await db.get(model, pk)
    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found.")
    return record

async def create_record(db: Session, data: dict, model):
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
    record = await db.get(model, pk)
    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found.")

    await db.delete(record)
    await db.commit()

    return {"detail": f"{model.__name__} deleted successfully."}

async def update_record_by_composite_key(db: Session, pk: dict, new_data: dict, model):
    """
    pk: dict of primary key fields, e.g. {"user_id": "CST000123", "service_id": 42}
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
    pk: dict of primary key fields, e.g. {"user_id": "CST000123", "service_id": 42}
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
