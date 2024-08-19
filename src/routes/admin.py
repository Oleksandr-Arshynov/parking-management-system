from src.database.models import Car, User
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
    "/delete-user/{user_id}", dependencies=[Depends(auth_service.require_role())]
)
def delete_user(
    user_id: int,
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
from src.database.models import Car
from src.database.db import get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

admin_router = APIRouter(prefix="/admin", tags=["admin"])


# @admin_router.delete("/vehicles/{license_plate}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_vehicle(license_plate: str, db: Session = Depends(get_db)):
#     vehicle = db.query(Car).filter(Car.license_plate == license_plate).first()
#     if vehicle is None:
#         raise HTTPException(status_code=404, detail="Vehicle not found")
    
#     db.delete(vehicle)
#     db.commit()
#     return {"detail": "Vehicle deleted successfully"}

# @admin_router.put("/vehicles/{license_plate}/rate", response_model=Car)
# def update_parking_rate(license_plate: str, rate_update: ParkingRateUpdate, db: Session = Depends(get_db)):
#     vehicle = db.query(Car).filter(Car.license_plate == license_plate).first()
#     if vehicle is None:
#         raise HTTPException(status_code=404, detail="Vehicle not found")
    
#     vehicle.rate = rate_update.rate
    
#     db.commit()
#     db.refresh(vehicle)
#     return vehicle

# @admin_router.put("/blacklist", status_code=status.HTTP_200_OK)
# def update_blacklist_status(blacklist_update: BlacklistUpdate, db: Session = Depends(get_db)):
#     vehicle = db.query(Car).filter(Car.license_plate == blacklist_update.license_plate).first()
#     if vehicle is None:
#         raise HTTPException(status_code=404, detail="Vehicle not found")
    
#     vehicle.black_list = blacklist_update.black_list
    
#     db.commit()
#     db.refresh(vehicle)
#     return {"detail": "Blacklist status updated", "license_plate": vehicle.license_plate, "black_list": vehicle.black_list}
