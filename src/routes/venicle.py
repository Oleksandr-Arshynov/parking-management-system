from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.models import Car
from src.database.db import get_db

app = FastAPI()

@app.get("/car/{license_plate}")
def get_vehicle(license_plate: str, db: Session = Depends(get_db)):
    vehicle = db.query(Car).filter(Car.license_plate == license_plate).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle
