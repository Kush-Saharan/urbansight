import ee
import matplotlib.pyplot as plt

# Initialize Earth Engine

ee.Initialize(project="urbansight-ee")

# Delhi bounding box (LOCKED)

delhi_bbox = ee.Geometry.Rectangle([76.80, 28.40, 77.40, 28.90])

# Cloud masking function (QA60)

def mask_s2_clouds(image):
    qa = image.select("QA60")
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11

    mask = (
        qa.bitwiseAnd(cloud_bit_mask).eq(0)
        .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    )

    return image.updateMask(mask).divide(10000)

# NDVI for one year (Jan–Mar)
def yearly_ndvi(year):
    start = f"{year}-01-01"
    end   = f"{year}-03-31"

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(delhi_bbox)
        .filterDate(start, end)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(mask_s2_clouds)
    )

    image = collection.median()

    ndvi = (
        image.normalizedDifference(["B8", "B4"])
        .rename("NDVI")
        .clip(delhi_bbox)
    )

    stats = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=delhi_bbox,
        scale=10,
        maxPixels=1e9
    )

    return stats.get("NDVI")

# Run multi-year analysis
years = range(2019, 2025)
ndvi_results = {}

for y in years:
    value = yearly_ndvi(y).getInfo()
    ndvi_results[y] = value

print("Delhi NDVI (Winter: Jan–Mar)")
for y, v in ndvi_results.items():
    print(f"{y}: {v:.3f}" if v else f"{y}: No data")

# Plot NDVI trend
years = list(ndvi_results.keys())
values = list(ndvi_results.values())

plt.figure(figsize=(8, 5))
plt.plot(years, values, marker="o")
plt.xlabel("Year")
plt.ylabel("Average NDVI")
plt.title("Delhi NDVI Trend (Winter, Jan–Mar)")
plt.grid(True)
plt.tight_layout()
plt.show()
