import pandas as pd

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

def transform(record):
    df = pd.DataFrame([record])

    # Rename
    df = df.rename(columns={
        "temperature_c": "temp_c",
        "wind_speed_ms": "wind_ms",
        "description": "weather_desc",
        "fetched_at": "fetched_at_utc"
    })

    # Fix types
    df["fetched_at_utc"] = pd.to_datetime(df["fetched_at_utc"])

    # Fill missing
    df["weather_desc"] = df["weather_desc"].fillna("unknown")
    df["temp_c"] = df["temp_c"].fillna(0.0)

    # Transformations
    df["temp_f"] = df["temp_c"].apply(lambda x: round((x * 9/5) + 32, 2))
    df["wind_kmh"] = df["wind_ms"].apply(lambda x: round(x * 3.6, 2))
    df["comfort_level"] = df["temp_c"].apply(comfort_level)
    df["fetch_date"] = df["fetched_at_utc"].dt.date
    df["fetch_time"] = df["fetched_at_utc"].dt.time
    df["weather_desc"] = df["weather_desc"].apply(lambda x: x.title())

    return df