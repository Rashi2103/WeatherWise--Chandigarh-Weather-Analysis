"""Download observed historical daily weather for Chandigarh from Open-Meteo."""
from pathlib import Path
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "chandigarh_weather.csv"
URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch(start_date: str = "2019-01-01", end_date: str = "2025-12-31") -> pd.DataFrame:
    params = {
        "latitude": 30.7333,
        "longitude": 76.7794,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Asia/Kolkata",
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    daily = payload["daily"]
    df = pd.DataFrame({
        "date": daily["time"],
        "temperature_max_c": daily["temperature_2m_max"],
        "temperature_min_c": daily["temperature_2m_min"],
        "precipitation_mm": daily["precipitation_sum"],
    })
    df["date"] = pd.to_datetime(df["date"])
    df["precipitation_mm"] = df["precipitation_mm"].fillna(0).clip(lower=0)
    df["temperature_max_c"] = pd.to_numeric(df["temperature_max_c"], errors="coerce")
    df["temperature_min_c"] = pd.to_numeric(df["temperature_min_c"], errors="coerce")
    df = df.dropna(subset=["date", "temperature_max_c", "temperature_min_c"])
    df = df.drop_duplicates(subset=["date"]).sort_values("date")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False, date_format="%Y-%m-%d")
    print(f"Saved {len(df):,} observed daily records to {OUT}")
    print("Source: Open-Meteo Historical Weather API. Review its attribution/licence terms before redistribution.")
    return df


if __name__ == "__main__":
    fetch()
