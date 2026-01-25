import ee
import matplotlib.pyplot as plt

# 1. INITIALIZE EARTH ENGINE

ee.Initialize(project="urbansight-ee")
# 2. DELHI BOUNDING BOX (LOCKED)

MIN_LAT, MAX_LAT = 28.40, 28.90
MIN_LON, MAX_LON = 76.80, 77.40

delhi_bbox = ee.Geometry.Rectangle(
    [MIN_LON, MIN_LAT, MAX_LON, MAX_LAT]
)

# 3. SENTINEL-2 CLOUD MASKING (QA60)

def mask_s2_clouds(image):
    qa = image.select("QA60")

    cloud_bit = 1 << 10
    cirrus_bit = 1 << 11

    mask = (
        qa.bitwiseAnd(cloud_bit).eq(0)
        .And(qa.bitwiseAnd(cirrus_bit).eq(0))
    )

    return image.updateMask(mask).divide(10000)

# 4. CREATE 5x5 GRID ZONES OVER DELHI

GRID_SIZE = 5
lat_step = (MAX_LAT - MIN_LAT) / GRID_SIZE
lon_step = (MAX_LON - MIN_LON) / GRID_SIZE

zones = []
zone_id = 0

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        zone_id += 1

        lat1 = MIN_LAT + i * lat_step
        lat2 = lat1 + lat_step
        lon1 = MIN_LON + j * lon_step
        lon2 = lon1 + lon_step

        geom = ee.Geometry.Rectangle([lon1, lat1, lon2, lat2])
        zones.append((f"Z{zone_id:02}", geom))

# 5. NDVI FOR A SINGLE ZONE & YEAR (JAN–MAR)

def zonal_ndvi(zone_geom, year):
    start = f"{year}-01-01"
    end   = f"{year}-03-31"

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(zone_geom)
        .filterDate(start, end)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(mask_s2_clouds)
    )

    image = collection.median()

    ndvi = (
        image.normalizedDifference(["B8", "B4"])
        .rename("NDVI")
    )

    stats = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=zone_geom,
        scale=10,
        maxPixels=1e9
    )

    return stats.get("NDVI")

# 6. RUN MULTI-YEAR ZONAL NDVI (2019–2024)

YEARS = range(2019, 2025)

zone_ndvi = {}

for zone_name, zone_geom in zones:
    zone_ndvi[zone_name] = {}

    for year in YEARS:
        value = zonal_ndvi(zone_geom, year).getInfo()
        zone_ndvi[zone_name][year] = value

# 7. PRINT RESULTS (CLEAN FORMAT)

print("\nZonal NDVI (Winter: Jan–Mar)\n")

for zone, values in zone_ndvi.items():
    print(zone, ":", end=" ")
    for year, ndvi in values.items():
        if ndvi is not None:
            print(f"{year}={ndvi:.3f}", end="  ")
        else:
            print(f"{year}=NA", end="  ")
    print()

# 8. PLOT NDVI TREND FOR ONE ZONE (EXAMPLE)

ZONE_TO_PLOT = "Z07"

years = list(zone_ndvi[ZONE_TO_PLOT].keys())
values = list(zone_ndvi[ZONE_TO_PLOT].values())

plt.figure(figsize=(8, 5))
plt.plot(years, values, marker="o")
plt.xlabel("Year")
plt.ylabel("Average NDVI")
plt.grid(True)
plt.tight_layout()
plt.show()
