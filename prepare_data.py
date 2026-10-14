"""Clean weather CSV and load it into a queryable SQLite database."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent
CSV = ROOT / "data" / "chandigarh_weather.csv"
DB = ROOT / "weatherwise.db"
REQUIRED = ["date", "temperature_max_c", "temperature_min_c", "precipitation_mm"]


def prepare() -> pd.DataFrame:
    if not CSV.exists():
        raise FileNotFoundError(f"{CSV} not found. Run `python fetch_weather.py` first.")
    df = pd.read_csv(CSV)
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")
    df = df[REQUIRED].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in REQUIRED[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["precipitation_mm"] = df["precipitation_mm"].clip(lower=0)
    df = df.dropna(subset=REQUIRED).drop_duplicates(subset="date").sort_values("date")
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["temperature_range_c"] = df["temperature_max_c"] - df["temperature_min_c"]
    # These are simple screening flags for exploration, not official warnings.
    df["heavy_rain_day"] = (df["precipitation_mm"] >= 50).astype(int)
    df["hot_day"] = (df["temperature_max_c"] >= 40).astype(int)
    with sqlite3.connect(DB) as conn:
        df.to_sql("daily_weather", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_weather_date ON daily_weather(date)")
    print(f"Cleaned {len(df):,} records; database saved to {DB}")
    print(f"Date range: {df.date.min().date()} to {df.date.max().date()}")
    print(f"Rows removed as invalid/duplicate: {len(pd.read_csv(CSV)) - len(df)}")
    return df


if __name__ == "__main__":
    prepare()
