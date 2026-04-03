import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime,timezone

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not set")

CITY = "Charlottetown"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    exit(1)

data = response.json()

# Extract the fields you want
weather_record = {
    "city": data["name"],
    "country": data["sys"]["country"],
    "temperature_c": data["main"]["temp"],
    "feels_like_c": data["main"]["feels_like"],
    "humidity_pct": data["main"]["humidity"],
    "description": data["weather"][0]["description"],
    "wind_speed_ms": data["wind"]["speed"],
    "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
}

# Convert to DataFrame
df = pd.DataFrame([weather_record])

print(df)
print(df.dtypes)