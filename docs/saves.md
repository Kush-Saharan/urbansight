Delhi:

Latitude, longitude:
Lat: 28.6139
Lon: 77.2090

Bounding Box:
min_lat = 28.40
max_lat = 28.90
min_lon = 76.80
max_lon = 77.40

## Multi-Year NDVI (Delhi)

We computed average NDVI for Delhi using Sentinel-2
(B4, B8) for a fixed winter window (Jan–Mar) across
2019–2024 to ensure seasonal consistency.

Observed trend shows a gradual decline in average NDVI
after 2021, indicating potential loss of urban green cover.
This analysis captures correlation, not causation.

## Zonal NDVI Analysis (Delhi)

Delhi was divided into a 5×5 spatial grid.
Only zones intersecting the Delhi boundary were retained.

Average NDVI was computed per zone for winter
(Jan–Mar) across multiple years.

This enabled localized detection of green cover loss,
revealing spatial heterogeneity within the city.

## A. AQI / PM2.5 Data Processing

### Data Source
Kaggle dataset
Multiple stations (DL001–DL040)
Pollutant of interest: PM2.5 (µg/m³)

### Preprocessing Steps
Converted hourly timestamps to datetime
Extracted date from timestamp
Removed invalid / missing PM2.5 values
Filtered unrealistic values (negative / extreme outliers)
Aggregated to daily average PM2.5

### Seasonal Aggregation
Focused on winter season (Jan–Mar)
Computed winter-average PM2.5 per year
Aggregated spatially to zone–year level

## B. Spatial Zoning Strategy
### Motivation

Administrative boundaries introduce bias
Station density is uneven across Delhi

### Approach
Defined a fixed bounding box over Delhi
Divided into a 5×5 uniform grid (25 zones)
Each zone represents a consistent spatial unit across years

### Benefits:
Spatial consistency
No political boundary bias
Suitable for zonal environmental analysis

## D. Data Alignment & Merging

### Alignment Strategy
Matched zone + year between datasets
Ensured temporal overlap before merging

Merged dataset:
zone,year,pm25_winter,ndvi_winter
Z03,2019,105.21,0.265

Only overlapping zone–year pairs were used.

## E. Correlation Analysis

### Methods Used
Pearson correlation (linear relationship) : 0.085
Spearman correlation (rank-based, monotonic) : -0.015

### Key Insight
Vegetation cover, as measured by NDVI, shows negligible association with winter PM2.5 concentrations across Delhi zones.

### Reasons
PM2.5 dominated by emission sources and meteorology
NDVI effects are local and non-linear
Seasonal averaging smooths short-term vegetation effects

### Important Clarification
This study identifies association, not causation
Results do not imply vegetation has no benefit
Rather, its effect is not dominant at zonal–seasonal scale