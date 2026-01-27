import pandas as pd
from shapely.geometry import Point, box
import matplotlib.pyplot as plt

# =====================================================
# 1. LOAD DATA
# =====================================================
df = pd.read_csv("data/processed/pm25_daily_all_stations.csv")

# Parse date
df["date"] = pd.to_datetime(df["date"])

# Keep only winter months (Jan–Mar)
df = df[df["date"].dt.month.isin([1, 2, 3])]

# Add year
df["year"] = df["date"].dt.year

# =====================================================
# 2. DEFINE SAME DELHI GRID (5x5) — MUST MATCH NDVI
# =====================================================
MIN_LAT, MAX_LAT = 28.40, 28.90
MIN_LON, MAX_LON = 76.80, 77.40
GRID_SIZE = 5

lat_step = (MAX_LAT - MIN_LAT) / GRID_SIZE
lon_step = (MAX_LON - MIN_LON) / GRID_SIZE

zone_polygons = {}
zone_id = 0

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        zone_id += 1
        lat1 = MIN_LAT + i * lat_step
        lat2 = lat1 + lat_step
        lon1 = MIN_LON + j * lon_step
        lon2 = lon1 + lon_step

        zone_polygons[f"Z{zone_id:02}"] = box(lon1, lat1, lon2, lat2)

# =====================================================
# 3. ASSIGN ZONES TO STATIONS
# =====================================================
def assign_zone(lat, lon):
    p = Point(lon, lat)
    for zname, poly in zone_polygons.items():
        if poly.contains(p):
            return zname
    return None

df["zone"] = df.apply(
    lambda r: assign_zone(r["latitude"], r["longitude"]),
    axis=1
)

# Drop rows outside Delhi grid
df = df.dropna(subset=["zone"])

# =====================================================
# 4. COMPUTE ZONAL PM2.5 (WINTER MEAN)
# =====================================================
zonal_pm25 = (
    df.groupby(["zone", "year"])["pm25_avg"]
      .mean()
      .reset_index()
      .rename(columns={"pm25_avg": "pm25"})
      .sort_values(["zone", "year"])
)

print("\nZonal PM2.5 (Winter: Jan–Mar)\n")
print(zonal_pm25.head(10))

# =====================================================
# 5. SAVE FOR ML / CORRELATION STEP
# =====================================================
zonal_pm25.to_csv(
    "data/processed/zonal_pm25_winter.csv",
    index=False
)

# =====================================================
# 6. OPTIONAL: PLOT ONE ZONE
# =====================================================
ZONE_TO_PLOT = "Z07"

z = zonal_pm25[zonal_pm25["zone"] == ZONE_TO_PLOT]

if not z.empty:
    plt.figure(figsize=(8, 5))
    plt.plot(z["year"], z["pm25"], marker="o")
    plt.xlabel("Year")
    plt.ylabel("PM2.5 (µg/m³)")
    plt.title(f"PM2.5 Trend for {ZONE_TO_PLOT} (Delhi, Winter)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
