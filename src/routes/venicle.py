from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.models import Parking
from src.database.db import get_db

router = APIRouter(prefix="/car", tags=["car"])

@router.get("/car/{license_plate}")
def get_vehicle(license_plate: str, db: Session = Depends(get_db)):
    vehicle = db.query(Parking).filter(Parking.plate == license_plate).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

