import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
hourly_dir = Path("data/raw/air_quality/delhi_stations")
station_meta = pd.read_csv("data/processed/stations_with_lat_long.csv")

station_meta = station_meta.rename(columns={"file_name": "station_id"})

all_daily = []

# -----------------------------
# Process each station file
# -----------------------------
for file in hourly_dir.glob("DL*.csv"):
    station_id = file.stem  # DL027

    try:
        df = pd.read_csv(file)
    except Exception as e:
        print(f"❌ Could not read {file.name}: {e}")
        continue

    # Standard CPCB column names
    if "From Date" not in df.columns or "PM2.5 (ug/m3)" not in df.columns:
        print(f"⚠️ Skipping {file.name}: PM2.5 not found")
        continue

    # Rename & parse
    df = df.rename(columns={
        "From Date": "datetime",
        "PM2.5 (ug/m3)": "pm25"
    })

    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # Drop missing PM2.5
    df = df.dropna(subset=["pm25"])

    # Filter impossible values
    df = df[(df["pm25"] >= 0) & (df["pm25"] <= 1500)]

    if df.empty:
        print(f"⚠️ {station_id}: No valid PM2.5 data")
        continue

    # Daily aggregation
    df["date"] = df["datetime"].dt.date

    daily = (
        df
        .groupby("date", as_index=False)
        .agg(pm25_avg=("pm25", "mean"))
    )

    daily["station_id"] = station_id
    all_daily.append(daily)

# -----------------------------
# Combine all stations
# -----------------------------
if not all_daily:
    raise ValueError("❌ No valid PM2.5 data found in any station")

pm25_daily = pd.concat(all_daily, ignore_index=True)

# -----------------------------
# Merge lat / long
# -----------------------------
final = pm25_daily.merge(
    station_meta[["station_id", "latitude", "longitude"]],
    on="station_id",
    how="left"
)

# Round values
final["pm25_avg"] = final["pm25_avg"].round(2)

# -----------------------------
# Save output
# -----------------------------
final.to_csv("data/processed/pm25_daily_all_stations.csv", index=False)

print("✅ PM2.5 daily dataset created: pm25_daily_all_stations.csv")
