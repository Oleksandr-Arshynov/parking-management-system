from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.models import Plate, Parking
from src.database.db import get_db
from fastapi.responses import JSONResponse

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

#PARKING_COST_LIMIT = 100.00

app = FastAPI()

@app.get("/check-cost/{license_plate}")
def check_parking_cost(license_plate: str, db: Session = Depends(get_db)):
    # Отримуємо інформацію про транспортний засіб за номерним знаком
    vehicle = db.query(Plate).filter(Plate.license_plate == license_plate).first()
    
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    if Parking.total_cost > Plate.parking_limit:
        return JSONResponse(
            status_code=200,
            content={"message": f"Warning: Your parking cost has exceeded the limit of {Plate.parking_limit}. Current total: {Parking.total_cost}"},
        )
    
    return {"message": "Your parking cost is within the limit."}

# EMAIL

conf = ConnectionConfig(
    MAIL_USERNAME="your_username",
    MAIL_PASSWORD="your_password",
    MAIL_FROM="your_email@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.example.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
)

def send_email(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="plain"
    )
    fm = FastMail(conf)
    fm.send_message(message)

@app.get("/check-cost-email/{license_plate}")
def check_parking_cost(license_plate: str, db: Session = Depends(get_db)):
    vehicle = db.query(Plate).filter(Plate.license_plate == license_plate).first()
    
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    if Parking.total_cost > Plate.parking_limit:
        send_email(
            subject="Parking Cost Exceeded",
            email_to="user@example.com",  # email of the vehicle owner
            body=f"Warning: Your parking cost has exceeded the limit of {Plate.parking_limit}. Current total: {Parking.total_cost}"
        )
        return {"message": "Warning: Your parking cost has exceeded the limit. An email has been sent."}
    
    return {"message": "Your parking cost is within the limit."}
