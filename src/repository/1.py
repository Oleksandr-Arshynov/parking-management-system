from datetime import datetime, timedelta

class ParkingSystem:
    def __init__(self, hourly_rate=2.0):
        self.parking_records = {}
        self.hourly_rate = hourly_rate

    def vehicle_entry(self, license_plate):
        entry_time = datetime.now()
        self.parking_records[license_plate] = {"entry": entry_time}
        print(f"Vehicle {license_plate} entered at {entry_time}")

    def vehicle_exit(self, license_plate):
        if license_plate in self.parking_records and "entry" in self.parking_records[license_plate]:
            exit_time = datetime.now()
            entry_time = self.parking_records[license_plate]["entry"]
            self.parking_records[license_plate]["exit"] = exit_time
            duration = exit_time - entry_time
            self.parking_records[license_plate]["duration"] = duration
            print(f"Vehicle {license_plate} exited at {exit_time}")
            print(f"Total parking duration: {duration}")
        else:
            print(f"No entry record found for vehicle {license_plate}")

    def calculate_parking_fee(self, license_plate):
        if license_plate in self.parking_records and "duration" in self.parking_records[license_plate]:
            duration = self.parking_records[license_plate]["duration"]
            hours_parked = duration.total_seconds() / 3600
            fee = round(hours_parked * self.hourly_rate, 2)
            self.parking_records[license_plate]["fee"] = fee
            print(f"Total parking fee for vehicle {license_plate}: ${fee}")
            return fee
        else:
            print(f"No exit record found for vehicle {license_plate}")
            return 0.0

# Налаштування системи паркування з погодинною оплатою $3.0 за годину
parking_system = ParkingSystem(hourly_rate=3.0)

# Автомобіль в'їжджає на стоянку
parking_system.vehicle_entry("AB123CD")

# Автомобіль виїжджає зі стоянки
parking_system.vehicle_exit("AB123CD")

# Розрахунок плати за паркування
parking_system.calculate_parking_fee("AB123CD")