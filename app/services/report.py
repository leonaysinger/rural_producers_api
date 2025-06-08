from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.domain.models.crop import Crop
from app.domain.models.rural_property import RuralProperty
from app.domain.models.property_crop import PropertyCrop

def get_summary(db: Session) -> dict:
    total_farms = db.query(func.count(RuralProperty.id)).scalar()
    total_area = db.query(func.coalesce(func.sum(RuralProperty.total_area), 0)).scalar()
    return {
        "total_farms": int(total_farms),
        "total_area": float(total_area)
    }

def get_farms_by_state(db: Session) -> list[dict]:
    results = (
        db.query(RuralProperty.state, func.count(RuralProperty.id))
        .group_by(RuralProperty.state)
        .all()
    )
    return [{"name": state.upper(), "value": count} for state, count in results]

def get_farms_by_crop(db: Session) -> list[dict]:
    results = (
        db.query(Crop.name, func.count(PropertyCrop.id))
        .join(PropertyCrop, Crop.id == PropertyCrop.crop_id)
        .group_by(Crop.name)
        .all()
    )
    return [{"name": crop, "value": count} for crop, count in results]

def get_land_usage(db: Session) -> list[dict]:
    farming, vegetation = (
        db.query(
            func.coalesce(func.sum(RuralProperty.farming_area), 0),
            func.coalesce(func.sum(RuralProperty.vegetation_area), 0),
        )
        .one()
    )
    return [
        {"name": "Área Cultivável", "value": float(farming)},
        {"name": "Área de Vegetação", "value": float(vegetation)}
    ]
