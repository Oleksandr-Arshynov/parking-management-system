from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

class VehicleBase(BaseModel):
    license_plate: str
    owner_name: Optional[str] = None
    entry_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None
    parking_duration: Optional[str] = None
    total_cost: Optional[float] = None


class CarCreate(BaseModel):
    user_id: int
    license_plate: str
    black_list: Optional[bool] = False
    total_cost: Optional[float] = None
    parking_limit: Optional[float] = 1000
    

    class Config:
        orm_mode = True


class CarResponse(BaseModel):
    id: int
    license_plate: str
    user_id: int
    plate_id: int
    entry_time: Optional[datetime]
    exit_time: Optional[datetime]
    rate: float
    parking_duration: Optional[datetime]
    total_cost: Optional[float]
    finish_parking: Optional[bool]
    


    class Config:
        orm_mode = True
