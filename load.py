import sqlite3
import pandas as pd

def load(df):
    conn = sqlite3.connect("weather_data.db")
    
    df.to_sql(
        name="weather",
        con=conn,
        if_exists="append",
        index=False
    )

    df_check = pd.read_sql("SELECT * FROM weather", conn)
    print(f"Total rows in database: {len(df_check)}")
    
    conn.close()