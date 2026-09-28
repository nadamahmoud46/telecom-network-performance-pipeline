import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

from config import DB_CONFIG

# -----------------------------
# 1. Create Cities Data
# -----------------------------

cities_data = [
    {
        "city_id": 1,
        "city_name": "Cairo",
        "region": "Greater Cairo",
        "latitude": 30.0444,
        "longitude": 31.2357
    },
    {
        "city_id": 2,
        "city_name": "Giza",
        "region": "Greater Cairo",
        "latitude": 30.0131,
        "longitude": 31.2089
    },
    {
        "city_id": 3,
        "city_name": "Alexandria",
        "region": "North Coast",
        "latitude": 31.2001,
        "longitude": 29.9187
    },
    {
        "city_id": 4,
        "city_name": "Mansoura",
        "region": "Delta",
        "latitude": 31.0409,
        "longitude": 31.3785
    },
    {
        "city_id": 5,
        "city_name": "Tanta",
        "region": "Delta",
        "latitude": 30.7865,
        "longitude": 31.0004
    },
    {
        "city_id": 6,
        "city_name": "Aswan",
        "region": "Upper Egypt",
        "latitude": 24.0889,
        "longitude": 32.8998
    },
    {
        "city_id": 7,
        "city_name": "Luxor",
        "region": "Upper Egypt",
        "latitude": 25.6872,
        "longitude": 32.6396
    },
    {
        "city_id": 8,
        "city_name": "Port Said",
        "region": "Canal",
        "latitude": 31.2653,
        "longitude": 32.3019
    },
    {
        "city_id": 9,
        "city_name": "Suez",
        "region": "Canal",
        "latitude": 29.9668,
        "longitude": 32.5498
    },
    {
        "city_id": 10,
        "city_name": "Sharm El Sheikh",
        "region": "Sinai",
        "latitude": 27.9158,
        "longitude": 34.3300
    }
]


cities_df = pd.DataFrame(cities_data)


# -----------------------------
# 2. Save as Parquet
# -----------------------------

output_path = Path("../data/parquet/cities.parquet")

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

cities_df.to_parquet(
    output_path,
    index=False
)

print("Cities parquet created successfully")


# -----------------------------
# 3. Load into PostgreSQL
# -----------------------------

connection_string = (
    f"postgresql+psycopg://"
    f"{DB_CONFIG['user']}:"
    f"{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:"
    f"{DB_CONFIG['port']}/"
    f"{DB_CONFIG['database']}"
)

print(connection_string)

engine = create_engine(connection_string)


cities_df.to_sql(
    name="cities",
    con=engine,
    schema="network",
    if_exists="append",
    index=False
)


print("Cities loaded into PostgreSQL successfully")