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
    """
    Retrieve vehicle information based on the license plate.

    - **license_plate**: The license plate number of the vehicle to retrieve.
    - **db**: SQLAlchemy database session.
    - **current_user**: The currently authenticated user.

    Returns:
    - **200 OK**: The details of the vehicle if found.
    - **404 Not Found**: If no vehicle is found with the provided license plate.
    - **403 Forbidden**: If the current user does not have admin privileges.

    Raises:
    - **HTTPException**: With status code 404 if the vehicle is not found.
    - **HTTPException**: With status code 403 if the user does not have sufficient permissions.
    """
    is_admin(current_user)
    vehicle = db.query(Plate).filter(Plate.license_plate == license_plate).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

