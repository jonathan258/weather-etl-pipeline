import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("weather_data.db")

# ── Query 1: See all data ─────────────────────────────────────────
print("=== All Weather Records ===")
df_all = pd.read_sql("SELECT * FROM weather", conn)
print(df_all)
print(f"Total rows: {len(df_all)}\n")

# ── Query 2: Average temperature and humidity ─────────────────────
print("=== Averages ===")
df_avg = pd.read_sql("""
    SELECT
        city,
        ROUND(AVG(temp_c), 2) AS avg_temp_c,
        ROUND(AVG(temp_f), 2) AS avg_temp_f,
        ROUND(AVG(humidity_pct), 2) AS avg_humidity
    FROM weather
    GROUP BY city
""", conn)
print(df_avg)
print()

# ── Query 3: Min and Max temperature ─────────────────────────────
print("=== Min and Max Temperature ===")
df_minmax = pd.read_sql("""
    SELECT
        city,
        ROUND(MIN(temp_c), 2) AS min_temp_c,
        ROUND(MAX(temp_c), 2) AS max_temp_c,
        ROUND(MIN(feels_like_c), 2) AS min_feels_like,
        ROUND(MAX(feels_like_c), 2) AS max_feels_like
    FROM weather
    GROUP BY city
""", conn)
print(df_minmax)
print()

# ── Query 4: Count records by comfort level ───────────────────────
print("=== Records by Comfort Level ===")
df_comfort = pd.read_sql("""
    SELECT
        comfort_level,
        COUNT(*) AS total_records
    FROM weather
    GROUP BY comfort_level
    ORDER BY total_records DESC
""", conn)
print(df_comfort)
print()

# ── Query 5: Most recent record ───────────────────────────────────
print("=== Most Recent Record ===")
df_latest = pd.read_sql("""
    SELECT *
    FROM weather
    ORDER BY fetched_at_utc DESC
    LIMIT 1
""", conn)
print(df_latest)
print()

# ── Query 6: Average wind speed ───────────────────────────────────
print("=== Wind Summary ===")
df_wind = pd.read_sql("""
    SELECT
        city,
        ROUND(AVG(wind_kmh), 2) AS avg_wind_kmh,
        ROUND(MIN(wind_kmh), 2) AS min_wind_kmh,
        ROUND(MAX(wind_kmh), 2) AS max_wind_kmh
    FROM weather
    GROUP BY city
""", conn)
print(df_wind)

# Close connection
conn.close()