from pydantic import BaseModel
from datetime import datetime

class LaptopDataSchema(BaseModel):
    laptop_id: str
    battery_level: int
    charging_status: bool
    last_on_time: datetime
    cpu_temperature: float
    cpu_speed: int
    memory_usage: int
    disk_usage: int
    network_status: str
    cpu_load: int

    class Config:
        from_attributes = True
