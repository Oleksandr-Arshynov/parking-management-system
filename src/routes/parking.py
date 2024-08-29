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
    content = await file.read()    
    nparr = np.fromstring(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    plate_recognized, plate_img =  plate_recognition.get_plate_number(img)
    plate = db.query(Plate).filter(Plate.license_plate == plate_recognized).first()
    
    if plate is None:
        return plate_img
        return {"filename": plate_recognized}
        raise HTTPException(status_code=404, detail=messages.PLATE_NOT_REGISTERED)
    elif plate:
        parking = db.query(Parking).filter(Parking.plate_id == plate.id, Parking.finish_parking == False).first()
        if parking:
            exit = await parking_exit(parking.id, db)
            return exit 
        elif not parking:
            enter = await parking_entry(plate.id, db)
            return enter 



    return plate_img