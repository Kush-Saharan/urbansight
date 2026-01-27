import ee
import pandas as pd

# ------------------------------------
# 1. INIT
# ------------------------------------
ee.Initialize(project="urbansight-ee")

# ------------------------------------
# 2. DELHI BOUNDING BOX
# ------------------------------------
MIN_LAT, MAX_LAT = 28.40, 28.90
MIN_LON, MAX_LON = 76.80, 77.40

# ------------------------------------
# 3. GRID SETUP
# ------------------------------------
GRID_SIZE = 5
lat_step = (MAX_LAT - MIN_LAT) / GRID_SIZE
lon_step = (MAX_LON - MIN_LON) / GRID_SIZE

zones = []
zone_id = 0

for i in range(GRID_SIZE):        # south → north
    for j in range(GRID_SIZE):    # west → east
        zone_id += 1

        lat1 = MIN_LAT + i * lat_step
        lat2 = lat1 + lat_step
        lon1 = MIN_LON + j * lon_step
        lon2 = lon1 + lon_step

        geom = ee.Geometry.Rectangle([lon1, lat1, lon2, lat2])
        zones.append(ee.Feature(geom, {"zone": f"Z{zone_id:02}"}))

zones_fc = ee.FeatureCollection(zones)

# ------------------------------------
# 4. NDVI FOR ONE ZONE + YEAR (ROBUST)
# ------------------------------------
def ndvi_zone_year(feature, year):
    geom = feature.geometry()

    start = ee.Date.fromYMD(year, 1, 1)
    end   = ee.Date.fromYMD(year, 3, 31)

    img = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(geom)
        .filterDate(start, end)
        .select(["B4", "B8"])
        .median()
    )

    ndvi = img.normalizedDifference(["B8", "B4"])

    value = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=500,          # <- key
        bestEffort=True
    )

    return feature.set({
        "year": year,
        "ndvi_winter": value.get("nd")
    })

# ------------------------------------
# 5. RUN ALL YEARS
# ------------------------------------
features = []

for year in range(2019, 2025):
    fc_year = zones_fc.map(lambda f: ndvi_zone_year(f, year))
    features.append(fc_year)

final_fc = ee.FeatureCollection(features).flatten()

# ------------------------------------
# 6. FETCH ONCE
# ------------------------------------
data = final_fc.getInfo()

# ------------------------------------
# 7. TO DATAFRAME
# ------------------------------------
rows = []
for f in data["features"]:
    p = f["properties"]
    rows.append({
        "zone": p["zone"],
        "year": p["year"],
        "ndvi_winter": p["ndvi_winter"]
    })

df = pd.DataFrame(rows)
df.to_csv("data/processed/zonal_pm25_winter.csv", index=False)

print("NDVI extraction complete")
print(df.head())
