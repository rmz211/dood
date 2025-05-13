# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import LaptopData
from schemas import LaptopDataSchema
import json
import sqlite3


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    init_db()

templates = Jinja2Templates(directory="templates")

@app.post("/laptop_data/")
async def receive_laptop_data(data: LaptopDataSchema, db: Session = Depends(get_db)):
    laptop_data = LaptopData(
        laptop_id=data.laptop_id,
        battery_level=data.battery_level,
        charging_status=data.charging_status,
        last_on_time=data.last_on_time,
        cpu_temperature=data.cpu_temperature,
        cpu_speed=data.cpu_speed,
        memory_usage=data.memory_usage,
        disk_usage=data.disk_usage,
        network_status=data.network_status,
        cpu_load=data.cpu_load
    )
    db.add(laptop_data)
    db.commit()
    return {"status": "Данные успешно получены"}

@app.get("/", response_class=HTMLResponse)
async def read_laptops(request: Request, db: Session = Depends(get_db)):
    laptops = db.query(LaptopData).all()
    battery_levels = [laptop.battery_level for laptop in laptops]
    battery_levels_json = json.dumps(battery_levels)  # в строку JSON
    return templates.TemplateResponse("index.html", {
        "request": request,
        "laptops": laptops,
        "battery_levels_json": battery_levels_json
    })

@app.post("/clear-data")
async def clear_database():
    file_path = 'laptops.sql'
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        cursor.execute(f"DELETE FROM {table[0]};")
    connection.commit()
    connection.close()
    return {"status": "Данные очищены"}