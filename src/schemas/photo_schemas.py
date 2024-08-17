from pydantic import BaseModel
from typing import List, Optional

from src.schemas.user_schemas import User


class PhotoBase(BaseModel):
    user_id: int
    photo: str
    description: Optional[str] = None

class Photo(PhotoBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    user: User


class PhotoUpdate(PhotoBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    user: User

    class Config:
        from_attributes = True
