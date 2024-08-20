from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta

app = FastAPI()

class ParkingSystem:
    def __init__(self, hourly_rate=2.0):
        self.parking_records = {}
        self.hourly_rate = hourly_rate

    def vehicle_entry(self, license_plate: str):
        entry_time = datetime.now()
        self.parking_records[license_plate] = {"entry": entry_time}
        return {"message": f"Vehicle {license_plate} entered at {entry_time}"}

    def vehicle_exit(self, license_plate: str):
        if license_plate in self.parking_records and "entry" in self.parking_records[license_plate]:
            exit_time = datetime.now()
            entry_time = self.parking_records[license_plate]["entry"]
            self.parking_records[license_plate]["exit"] = exit_time
            duration = exit_time - entry_time
            self.parking_records[license_plate]["duration"] = duration
            return {"message": f"Vehicle {license_plate} exited at {exit_time}", "duration": str(duration)}
        else:
            raise HTTPException(status_code=404, detail=f"No entry record found for vehicle {license_plate}")

    def calculate_parking_fee(self, license_plate: str):
        if license_plate in self.parking_records and "duration" in self.parking_records[license_plate]:
            duration = self.parking_records[license_plate]["duration"]
            hours_parked = duration.total_seconds() / 3600
            fee = round(hours_parked * self.hourly_rate, 2)
            self.parking_records[license_plate]["fee"] = fee
            return {"license_plate": license_plate, "parking_fee": fee}
        else:
            raise HTTPException(status_code=404, detail=f"No exit record found for vehicle {license_plate}")

# Ініціалізація системи паркування
parking_system = ParkingSystem(hourly_rate=3.0)

@app.post("/entry")
async def vehicle_entry(license_plate: str):
    return parking_system.vehicle_entry(license_plate)

@app.post("/exit")
async def vehicle_exit(license_plate: str):
    return parking_system.vehicle_exit(license_plate)

@app.post("/calculate-fee")
async def calculate_parking_fee(license_plate: str):
    return parking_system.calculate_parking_fee(license_plate)
