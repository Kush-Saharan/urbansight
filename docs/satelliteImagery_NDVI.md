## Satellite Imagery + NDVI
A band is an image captured in a specific wavelength range of light.

### Red Band: 
- Visible red light
- Vegetation absorbs red light for photosynthesis
- Healthy plants → low red reflectance

### Near InfraRed(NIR) band:
- Invisible to humans
- Vegetation strongly reflects NIR
- Healthy plants → high NIR reflectance

### NDVI(Normalized Difference Vegetation Index)
NDVI = (NIR - Red) / (NIR + Red)

NDVI captures:
“How much more NIR is reflected than Red”

Which directly corresponds to:
- Plant density
- Plant health
- Green cover presence

The division by (NIR + Red):
- Cancels lighting differences
- Cancels seasonal brightness changes
- Makes values comparable across time

## How to compute NDVI
For each pixel:
NDVI_pixel = (NIR_pixel - Red_pixel) / (NIR_pixel + Red_pixel)

We do this for :
- Thousands or millions of pixels
- Automatically (vectorized)

We get a new image:
- Same width & height
- Each pixel = NDVI value

This NDVI image gives a vegetation map.

### How to average NDVI over an areaHow to average NDVI over an area

- Step 1: Mask to city/zone

Use a city GeoJSON
Keep only NDVI pixels inside:
the city
or a specific grid zone

- Step 2: Collect valid NDVI values

Ignore:
water pixels
no-data pixels

Keep:
NDVI > 0 (usually vegetation)

- Step 3: Compute mean
Average NDVI = sum(NDVI pixels) / count(pixels)

By doing this we get one number per time period for each area.

### We use Sentinel-2 Bands
- B4    Red     Visible red light
- B8    NIR     Near-infrared


