from src.database.models import User
from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
 
)
from sqlalchemy.orm import Session
from src.database.db import get_db

from src.conf.config import settings
import cloudinary.uploader
from src.conf import messages
from src.auth.dependencies_auth import auth_service


router = APIRouter(prefix="/admin", tags=["admin"])

# Ендпоінт видалення користувача за ID
@router.delete(
    "/delete-plate/{license_plate}", dependencies=[Depends(auth_service.require_role())]
)
def delete_user(
    license_plate: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Deletes a user based on their unique identifier.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        dict: Confirmation message of the deleted user.
    """
    if current_user.role_id == 1:
        user = db.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=messages.ACCESS_FORBIDDEN,
        )
    db.delete(user)
    db.commit()

    return {"msg": f"Користувач {user.username} видалений"}

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import User, Plate, Parking
from src.schemas.car_schemas import CarCreate, CarResponse

router = APIRouter(prefix="/car", tags=["car"])

def is_admin(user: User):
    if user.role.role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

def is_user(user: User):
    if user.role.role != "User":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

# Admin Functions

@router.post("/add_plate", status_code=status.HTTP_201_CREATED)
def add_plate(plate: CarCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    is_admin(current_user)
    existing_plate = db.query(Plate).filter(Plate.license_plate == plate.license_plate).first()
    if existing_plate:
        raise HTTPException(status_code=400, detail="Vehicle with this license plate already exists")
    
    new_plate = Plate(
        user_id=plate.user_id,
        license_plate=plate.license_plate,
        black_list=plate.black_list,
        total_cost=plate.total_cost,
        parking_limit=plate.parking_limit
    )
    db.add(new_plate)
    db.commit()
    db.refresh(new_plate)
    return {"detail": "Plate added successfully"}

@router.delete("/delete_plate/{license_plate}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plate(license_plate: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    is_admin(current_user)
    plate = db.query(Plate).filter(Plate.license_plate == license_plate).first()
    if plate is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(plate)
    db.commit()
    return {"detail": "Plate deleted successfully"}

@router.put("/set_rate", status_code=status.HTTP_200_OK)
def set_parking_rate(plate_id: int, rate: float, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    is_admin(current_user)
    plate = db.query(Parking).filter(Parking.id == plate_id).first()
    if plate is None:
        raise HTTPException(status_code=404, detail="Parking record not found")
    
    plate.rate = rate
    db.commit()
    return {"detail": "Parking rate updated successfully"}

@router.put("/blacklist/{license_plate}", status_code=status.HTTP_200_OK)
def blacklist_vehicle(license_plate: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    is_admin(current_user)
    plate = db.query(Plate).filter(Plate.license_plate == license_plate).first()
    if plate is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    plate.black_list = True
    db.commit()
    return {"detail": "Vehicle blacklisted successfully"}


