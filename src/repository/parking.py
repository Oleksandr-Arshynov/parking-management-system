from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.database.models import User
from sqlalchemy.ext.declarative import declarative_base
from src.database.models import Parking, Plate

from src.conf import messages


async def parking_entry(plate_id: int, db: Session):
# Example usage
    found_palte = db.query(Plate).filter(Plate.id == plate_id).first() 
    new_parking = Parking(
        user_id= found_palte.user_id,  # Replace with actual user_id
        plate_id= plate_id,  # Replace with actual plate_id
        rate=20,  # Replace with actual rate
        entry_time=datetime.now(),  # Replace with actual entry time
        parking_duration=None,  # Calculate and set parking duration
        total_cost=0.0,  # Calculate and set total cost
        finish_parking=False  # Replace with actual finish_parking status
    )

    db.add(new_parking)
    db.commit()
    db.refresh(new_parking)
    return new_parking.id

async def parking_exit(parking_id:int, db: Session):
    found_parking = db.query(Parking).filter(Parking.id == parking_id).first()
    found_parking.exit_time = datetime.now()
    found_parking.parking_duration = found_parking.exit_time - found_parking.entry_time
    found_parking.total_cost = found_parking.rate * found_parking.parking_duration.total_seconds() / 3600.0
    found_parking.finish_parking = True

    found_plate = db.query(Plate).filter(Plate.id == found_parking.plate_id).first()
    found_plate.total_cost = found_plate.total_cost + found_parking.total_cost
    
    db.commit()

    if found_plate.total_cost > found_plate.parking_limit:
        raise HTTPException(status_code=402, detail=messages.REACHED_PARKING_LIMIT)
    
    db.commit()

    return found_parking.id