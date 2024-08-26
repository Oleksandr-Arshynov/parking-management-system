from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy.orm import Session
from src.database.models import Parking
from src.database.db import get_db
from fastapi.responses import StreamingResponse
import csv
import io


router = APIRouter(prefix="/report", tags=["report"])

@router.get("/generate-report/")
def generate_report(db: Session = Depends(get_db)):
    vehicles = db.query(Parking).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Номерний знак', 'Власник', 'Час вʼїзду', 'Час виїзду', 'Тривалість паркування', 'Загальна вартість'])

    for vehicle in vehicles:
        writer.writerow([vehicle.id, vehicle.plate_id, vehicle.user_id, vehicle.entry_time, vehicle.exit_time, vehicle.parking_duration, vehicle.total_cost])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=report.csv"})
