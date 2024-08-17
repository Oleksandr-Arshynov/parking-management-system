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
