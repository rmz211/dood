import psutil
import requests
from datetime import datetime
import time

API_URL = "http://127.0.0.1:8000/laptop_data/"

def collect_data():
    battery = psutil.sensors_battery()
    if battery is None:
        print("Не удалось получить данные о батарее.")
        return None

    cpu_temp = None
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures().get("coretemp", [None])
        cpu_temp = temps[0].current if temps and temps[0] else None

    cpu_freq = psutil.cpu_freq().current  # Скорость CPU
    network_status = "Up" if any(psutil.net_if_stats()[iface].isup for iface in psutil.net_if_stats()) else "Down"
    cpu_load = round(psutil.cpu_percent())
    memory_usage = round(psutil.virtual_memory().percent)
    disk_usage = round(psutil.disk_usage('/').percent)

    return {
        "laptop_id": "Nout-111",
        "battery_level": battery.percent,
        "charging_status": battery.power_plugged,
        "last_on_time": datetime.now().isoformat(),
        "cpu_temperature": cpu_temp or 0.0,
        "cpu_speed": round(cpu_freq),
        "network_status": network_status,
        "cpu_load": cpu_load,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage
    }


def send_data():
    data = collect_data()
    if data is None:
        print("Данные не собраны. Пропуск отправки.")
        return
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            print("Данные успешно отправлены на сервер")
        else:
            print(f"Не удалось отправить данные: статус {response.status_code}, ответ: {response.text}")
    except Exception as e:
        print(f"Ошибка при отправке данных: {e}")

if __name__ == "__main__":
    while True:
        send_data()
        time.sleep(30) # 15 сек
