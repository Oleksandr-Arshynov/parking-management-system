from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VehicleBase(BaseModel):
    license_plate: str
    owner_name: Optional[str] = None
    entry_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None
    parking_duration: Optional[str] = None
    total_cost: Optional[float] = None
