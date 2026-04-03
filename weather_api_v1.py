import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime,timezone
#Hello everyone, this is my first attempt at building an ETL pipeline.
# I am going to be using the OpenWeather API to extract weather data for Charlottetown, PEI.
# I will then clean and transform the data before loading it into a SQLite database.
#Please note that this is version 1 of the pipeline and there may be some bugs or issues 
# that I will need to fix in future versions.
#This is for my own teaching moment to use for self learning 
#Feel free to uses main.py as the main source of the true pipleline and to run thec code 
#Thank you

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

# ── Day 4: Clean ─────────────────────────────────────────

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

# ── Day 4: Transform ─────────────────────────────────────────

#Tranform the temp from celsius to fahrenheit
df["temp_f"] =df["temp_c"].apply(lambda temp_change:(temp_change *9/5)+32)

#Next is to change the wind speed from m/s to km/h
df["wind_kmh"] = df["wind_ms"].apply(lambda wind_change: wind_change * 3.6)


#Categorize the weather comfort levels based on the temperature outside

def comfort_level(temp):
    if temp < -10:
        return "Extreme Cold"
    elif temp < 0:
        return "Very Cold"
    elif temp < 10:
        return "Cold"
    elif temp < 20:
        return "Cool"
    elif temp < 30:
        return "Warm"
    else:
        return "Hot"
df["comfort_level"] = df["temp_c"].apply(comfort_level)

#Will need to extract the date and time from the fetched_at_utc column to create separate columns for date and time
df["fetch_date"] =df["fetched_at_utc"].dt.date
df["fetch_time"] = df["fetched_at_utc"].dt.time

#Make the weather description all uppercase for better readability
df["weather_desc"] = df["weather_desc"].apply(lambda x: x.title())

print("=== Transformed DataFrame ===")
pd.set_option("display.max_columns", None)
print(df)

print("\n=== Column Types ===")
print(df.dtypes)


