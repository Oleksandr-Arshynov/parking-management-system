from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.models import Plate, Parking
from src.database.db import get_db
from fastapi.responses import JSONResponse


#PARKING_COST_LIMIT = 100.00

router = APIRouter(prefix="/message", tags=["message"])

@router.get("/check-cost/{license_plate}")
def check_parking_cost(license_plate: str, db: Session = Depends(get_db)):
   
    vehicle = db.query(Plate).filter(Plate.license_plate == license_plate).first()
    
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    if Parking.total_cost > Plate.parking_limit:
        return JSONResponse(
            status_code=200,
            content={"message": f"Warning: Your parking cost has exceeded the limit of {Plate.parking_limit}. Current total: {Parking.total_cost}"},
        )
    
    return {"message": "Your parking cost is within the limit."}
