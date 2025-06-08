from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.services.report import get_summary, get_farms_by_state, get_farms_by_crop, get_land_usage

router = APIRouter(prefix="/reports", tags=["Reports"], dependencies=[Depends(get_current_user)])


@router.get("/summary")
def statistics_summary(db: Session = Depends(get_db)):
    return get_summary(db)


@router.get("/farms-by-state")
def statistics_by_state(db: Session = Depends(get_db)):
    return get_farms_by_state(db)


@router.get("/farms-by-crop")
def statistics_by_crop(db: Session = Depends(get_db)):
    return get_farms_by_crop(db)


@router.get("/land-usage")
def statistics_land_usage(db: Session = Depends(get_db)):
    return get_land_usage(db)
