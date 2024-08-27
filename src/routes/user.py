from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Parking, Plate, User
from src.repository import user as repository_user
from src.auth.dependencies_auth import auth_service
from src.routes.admin import is_user
from src.schemas.car_schemas import CarResponse

router = APIRouter(prefix="/user", tags=["user"])

# OK
@router.get("")
async def get_me_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Retrieve information of the currently authenticated user.

    - **db**: SQLAlchemy database session.
    - **current_user**: The currently authenticated user.

    Returns:
    - **200 OK**: The user's information.
    - **404 Not Found**: If the user is not found.
    """
    user = await repository_user.get_user(current_user.id, db)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# OK

# User Functions

@router.get("/my_plate", response_model=CarResponse)
def get_user_plate(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Get the registered plate information for the currently authenticated user.

    - **db**: SQLAlchemy database session.
    - **current_user**: The currently authenticated user.

    Returns:
    - **200 OK**: The user's plate information.
    - **404 Not Found**: If no plate is registered for the user.
    """
    is_user(current_user)
    plate = db.query(Plate).filter(Plate.user_id == current_user.id).first()
    if plate is None:
        raise HTTPException(status_code=404, detail="No registered plate found")
    
    return plate

@router.get("/parking_history", response_model=List[CarResponse])
def get_parking_history(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Get the parking history for the currently authenticated user.

    - **db**: SQLAlchemy database session.
    - **current_user**: The currently authenticated user.

    Returns:
    - **200 OK**: A list of parking records for the user.
    - **404 Not Found**: If no parking history is found for the user.
    """
    is_user(current_user)
    history = db.query(Parking).filter(Parking.user_id == current_user.id).all()
    if not history:
        raise HTTPException(status_code=404, detail="No parking history found")
    
    return history