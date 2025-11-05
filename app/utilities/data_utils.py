from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select
from app.schemas import PriceChartResponseWithService
from app.models import Service, Role

async def get_role_id(db: Session, role: str):
    result = await db.execute(select(Role).where(Role.role_name.ilike(role)))
    role_obj = result.scalar_one_or_none()
    return role_obj.id

def filter_data_for_model(model, data: dict):
    valid_keys = {c.name for c in model.__table__.columns}
    return {k: v for k, v in data.items() if k in valid_keys}

def serialize_service_response(service: Service):
    response = {
        "id": service.id,
        "title": service.title,
        "description": service.description,
        "works": service.works,
        "warranty_kms": service.warranty_kms,
        "warranty_months": service.warranty_months,
        "time_hrs": service.time_hrs,
        "difficulty": service.difficulty,
        "category": {
            "id": service.category.id,
            "name": service.category.name,
            "description": service.category.description
        },
        "price_chart": [
            PriceChartResponseWithService.from_orm(pc).model_dump()
            for pc in service.price_chart
        ],
        "fuel_types": [
            {"id": ft.id, "fuel_name": ft.fuel_name}
            for ft in service.fuel_types
        ],
        "created_at": service.created_at,
    }

    return response