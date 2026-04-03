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
#The next step in this is I am going to clean the data 

#Rename the columns 

df = df.rename(columns ={
    "temperature_c": "temp_c",
    "feels_like_c": "feels_like_c",
    "humidity_pct": "humidity_pct",
    "wind_speed_ms": "wind_ms",
    "description": "weather_desc",
    "fetched_at": "fetched_at_utc"
})

#change the fetched_at_utc to datetime format
df["fetched_at_utc"] = pd.to_datetime(df["fetched_at_utc"], format="%Y-%m-%d %H:%M:%S")

#Now I will check for missing values
print("==Null Check==")
print(df.isnull().sum())

#Fill missing values if any 
df["weather_desc"] = df["weather_desc"].fillna("unknown")
df["temp_c"] = df["temp_c"].fillna(0.0)

# Final output
print("\n=== Cleaned DataFrame ===")
pd.set_option("display.max_columns", None)
print(df)

print("\n=== Column Types ===")
print(df.dtypes)