from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession as Session
from typing import Dict, Any, Optional

async def get_all_records(
        db: Session,
        model: Any,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[InstrumentedAttribute] = None,
        desc: bool = False,
    ):
    query = select(model)

    # Apply filters dynamically
    if filters:
        for field_name, value in filters.items():
            if hasattr(model, field_name):
                field = getattr(model, field_name)
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

async def get_record_by_primary_key(db: Session, pk, model):
    record = await db.get(model, pk)
    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found.")
    return record

async def create_record(db: Session, data: dict, model):
    record = model(**data)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

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
