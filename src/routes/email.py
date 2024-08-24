from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.models import Plate, Parking, User
from src.database.db import get_db
from fastapi.responses import JSONResponse

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

router = APIRouter(prefix="/message-email", tags=["message-email"])

# conf налаштовано під gmail, внести свої дані !!! для решти пошт потрібно змінити налаштування див. нижче !!!
conf = ConnectionConfig(
    MAIL_USERNAME="your_username", 
    MAIL_PASSWORD="your_password", 
    MAIL_FROM="your_email@gmail.com", 
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com", 
    MAIL_TLS=True,
    MAIL_SSL=False,
    )              # For Outlook and other servers ---- change MAIL_TLS=False and MAIL_SSL=True

def send_email(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="plain"
    )
    fm = FastMail(conf)
    fm.send_message(message)

@router.get("/check-cost-email/{license_plate}")
def check_parking_cost(license_plate: str, db: Session = Depends(get_db)):
    vehicle = db.query(Plate).filter(Plate.license_plate == license_plate).first()
    
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    if Parking.total_cost > Plate.parking_limit:
        send_email(
            subject="Parking Cost Exceeded",
            email_to=User.email,  # email of the vehicle owner
            body=f"Warning: Your parking cost has exceeded the limit of {Plate.parking_limit}. Current total: {Parking.total_cost}"
        )
        return {"message": "Warning: Your parking cost has exceeded the limit. An email has been sent."}
    
    return {"message": "Your parking cost is within the limit."}