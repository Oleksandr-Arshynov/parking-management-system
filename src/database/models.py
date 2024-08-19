from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey, Boolean, Numeric, Interval

try:
    from src.database.db import Base
except:
    from database.db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String, nullable=True)
    confirmed = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('role.id'), default=3)
    number_of_car = Column(String(255))
    refresh_token = Column(String(255), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    role = relationship("Role", back_populates="user") 
    car = relationship("Car", back_populates="user")


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False, unique=True)

    user = relationship("User", back_populates="role") 


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    car = Column(String)
    public_id = Column(String)
    black_list = Column(Boolean)
    rate = Column(Float)
    entry_time = Column(DateTime) # Час заїзду
    exit_time = Column(DateTime) # Час виїзду
    license_plate = Column(String(10), unique=True, index=True) # Номерний знак авто
    parking_duration = Column(Interval) # Тривалість парковки
    total_cost = Column(Numeric(10, 2)) # Фінальна ціна парковки
    
    user = relationship("User", back_populates="car")  
    
