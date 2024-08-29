import cv2
from fastapi import APIRouter, FastAPI, HTTPException, Depends, File, UploadFile
import numpy as np
from sqlalchemy.orm import Session
from src.database.models import Plate, Parking
from src.database.db import get_db
from typing import Annotated
from src.repository import plate_recognition, parking
from fastapi.responses import JSONResponse, FileResponse
from src.conf import messages
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.repository.parking import parking_entry, parking_exit

router = APIRouter(prefix="/parking", tags=["parking"])



@router.post("/get_image/")
async def get_image(file: UploadFile, db: Session = Depends(get_db),):
    """
Uploads an image for license plate recognition and manages parking entries or exits based on the recognized plate.

Args:
    file (UploadFile): The image file containing the vehicle's license plate.
    db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

Returns:
    Response: The image with the recognized license plate highlighted, if successful.
    str: The recognized license plate if it is not registered.
    Raises:
        HTTPException: If the license plate is not registered in the database.
"""
    content = await file.read()    
    nparr = np.fromstring(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    plate_recognized, plate_img =  plate_recognition.get_plate_number(img)
    plate = db.query(Plate).filter(Plate.license_plate == plate_recognized).first()
    
    if plate is None:
        return plate_recognized
        raise HTTPException(status_code=404, detail=messages.PLATE_NOT_REGISTERED)
    elif plate:
        parking = db.query(Parking).filter(Parking.plate_id == plate.id, Parking.finish_parking == False).first()
        if parking:
            exit = await parking_exit(parking.id, db)
            return plate_img
        elif not parking:
            enter = await parking_entry(plate.id, db)
            return plate_img



    return plate_img