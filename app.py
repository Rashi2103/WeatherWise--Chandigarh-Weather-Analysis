from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

ROOT = Path(__file__).resolve().parent
CSV = ROOT / "data" / "chandigarh_weather.csv"
DB = ROOT / "weatherwise.db"

st.set_page_config(page_title="WeatherWise | Chandigarh", page_icon="🌦️", layout="wide")
st.title("🌦️ WeatherWise")
st.caption("Chandigarh weather explorer · Turning daily observations into science students can understand")
st.info("Educational analysis only. The 40°C heat and 50 mm daily-rain thresholds are exploratory flags for this project, not official IMD warnings or disaster predictions.")

@st.cache_data
def load_data():
    if DB.exists():
        with sqlite3.connect(DB) as conn:
            return pd.read_sql_query("SELECT * FROM daily_weather ORDER BY date", conn, parse_dates=["date"])
    if not CSV.exists():
        return pd.DataFrame()
    df = pd.read_csv(CSV, parse_dates=["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["temperature_range_c"] = df["temperature_max_c"] - df["temperature_min_c"]
    df["heavy_rain_day"] = (df["precipitation_mm"] >= 50).astype(int)
    df["hot_day"] = (df["temperature_max_c"] >= 40).astype(int)
    return df

df = load_data()
if df.empty:
    st.error("No weather data found. Run `python fetch_weather.py` and `python prepare_data.py`, then refresh this page.")
    st.stop()

min_year, max_year = int(df.date.dt.year.min()), int(df.date.dt.year.max())
years = list(range(min_year, max_year + 1))
selected_years = st.sidebar.select_slider("Choose year range", options=years, value=(years[0], years[-1]))
view = df[df.date.dt.year.between(selected_years[0], selected_years[1])].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Daily records", f"{len(view):,}")
c2.metric("Average daily high", f"{view.temperature_max_c.mean():.1f} °C")
c3.metric("Rainfall total", f"{view.precipitation_mm.sum():,.0f} mm")
c4.metric("Flagged heavy-rain days", f"{int(view.heavy_rain_day.sum()):,}")
st.caption(f"Period shown: {view.date.min().date()} to {view.date.max().date()} · Source is recorded in the data file's provenance and project README.")

left, right = st.columns(2)
with left:
    st.subheader("Temperature over time")
    temp = view.set_index("date")[["temperature_max_c", "temperature_min_c"]].resample("MS").mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(temp.index, temp.temperature_max_c, label="Average daily high")
    ax.plot(temp.index, temp.temperature_min_c, label="Average daily low")
    ax.set_ylabel("Temperature (°C)"); ax.set_xlabel("Month"); ax.legend(); ax.grid(alpha=.25)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)
with right:
    st.subheader("Monthly rainfall pattern")
    rain = view.groupby("month", as_index=False).agg(rainfall_mm=("precipitation_mm", "mean"))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(rain.month, rain.rainfall_mm)
    ax.set_xticks(range(1, 13)); ax.set_xlabel("Month"); ax.set_ylabel("Mean daily rainfall (mm)"); ax.grid(axis="y", alpha=.25)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)

st.subheader("Explore flagged weather days")
flags = view[(view.heavy_rain_day == 1) | (view.hot_day == 1)].copy()
flags["flag_type"] = flags.apply(lambda r: "Both" if r.heavy_rain_day and r.hot_day else ("Heavy rain" if r.heavy_rain_day else "Hot day"), axis=1)
st.write("These simple thresholds help students inspect unusual observations. They are not a substitute for official forecasts or local emergency guidance.")
if flags.empty:
    st.success("No days crossed either exploratory threshold in this selected period.")
else:
    st.dataframe(flags[["date", "temperature_max_c", "temperature_min_c", "precipitation_mm", "flag_type"]].sort_values("date", ascending=False), use_container_width=True, hide_index=True)

st.subheader("What might this mean?")
mean_rain = view.groupby("month").precipitation_mm.mean()
wet_month = int(mean_rain.idxmax()) if not mean_rain.empty else None
if wet_month:
    month_name = pd.Timestamp(2000, wet_month, 1).strftime("%B")
    st.markdown(f"- **Rainfall pattern:** In this selected period, **{month_name}** had the highest average daily rainfall of the calendar months shown. Compare years before drawing conclusions.")
st.markdown("- **For students:** Weather data is evidence, not certainty. A flagged day is a prompt to investigate, not proof that a flood, heatwave, or other disaster occurred.")
st.markdown("- **Next research step:** Compare observations with official event records and longer time periods before making risk claims.")

with st.expander("View SQL summary (database-backed when weatherwise.db exists)"):
    if DB.exists():
        with sqlite3.connect(DB) as conn:
            summary = pd.read_sql_query("SELECT year, ROUND(AVG(temperature_max_c),1) AS avg_daily_high_c, ROUND(SUM(precipitation_mm),1) AS rainfall_total_mm, SUM(heavy_rain_day) AS heavy_rain_days FROM daily_weather GROUP BY year ORDER BY year", conn)
        st.dataframe(summary, use_container_width=True, hide_index=True)
    else:
        st.write("Run `python prepare_data.py` to create the SQLite database and enable SQL-backed summaries.")

st.download_button("Download filtered observations (CSV)", view.to_csv(index=False).encode("utf-8"), file_name="weatherwise_filtered_data.csv", mime="text/csv")
st.caption("Built as a science-outreach portfolio project. Weather source: Open-Meteo Historical Weather API; see README for attribution and limitations.")
