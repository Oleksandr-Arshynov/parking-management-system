from pathlib import Path
from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.models import Plate, Parking, User
from src.database.db import get_db
from fastapi.responses import JSONResponse
from fastapi_mail.errors import ConnectionErrors
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.auth.dependencies_auth import auth_service

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.auth.dependencies_auth import conf
from src.routes.admin import is_admin

router = APIRouter(prefix="/message-email", tags=["message-email"])
                # For Outlook and other servers ---- change MAIL_TLS=False and MAIL_SSL=True

conf = ConnectionConfig(
    MAIL_USERNAME="fastapi_project@meta.ua",
    MAIL_PASSWORD="Pythoncourse2024",
    MAIL_FROM=str("fastapi_project@meta.ua"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="ContactManager",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path("./src/auth/templates"),)


async def send_email(email: str, username: str, host: str):
    try:
        token_verification = auth_service.create_email_token(data={"sub": email})
        message = MessageSchema(
            subject="Parking Cost Exceeded",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="parking_exceded.html")
    except ConnectionErrors as err:
        print(err)

@router.get("/check-cost-email/{license_plate}")
async def check_parking_cost(license_plate: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    is_admin(current_user)
    vehicle = db.query(Plate).filter(Plate.license_plate == license_plate).first()
    plate_ovner = db.query(User).filter(User.id == vehicle.user_id).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    if (vehicle.total_cost) > vehicle.parking_limit:
        await send_email(email=plate_ovner.email,username=plate_ovner.username,host = 'Check' )# email of the vehicle owner)
        return {"message": "Warning: Your parking cost has exceeded the limit. An email has been sent."}
    
    return {"message": "Your parking cost is within the limit."}