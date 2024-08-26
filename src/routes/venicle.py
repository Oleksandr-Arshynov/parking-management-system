from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.models import Parking, Plate
from src.database.models import User, Plate, Parking
from src.database.db import get_db
from src.routes.admin import is_admin
from src.auth.dependencies_auth import auth_service
router = APIRouter(prefix="/car", tags=["car"])



@router.get("/car/{license_plate}")
def get_vehicle(license_plate: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    is_admin(current_user)
    vehicle = db.query(Plate).filter(Plate.license_plate == license_plate).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

