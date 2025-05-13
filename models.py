from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from database import Base
from datetime import datetime

class LaptopData(Base):
    __tablename__ = "laptop_data"

    id = Column(Integer, primary_key=True, index=True)
    laptop_id = Column(String, index=True)
    battery_level = Column(Integer)
    charging_status = Column(Boolean)
    last_on_time = Column(DateTime, default=datetime.utcnow)
    cpu_temperature = Column(Float)
    cpu_speed = Column(Integer)
    memory_usage = Column(Integer)
    disk_usage = Column(Integer)
    network_status = Column(String)
    cpu_load = Column(Integer)
