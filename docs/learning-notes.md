## Geospatial Basic:

### Latitude and longitude:
- Latitude(lat): up-down positions on Earth
            Ranges from -90 to 90 degree
- Longitude(long):    left-right positions on earth
                Ranges from -180 to 180 degree

Every dataset we use(satellite, AQ stations, fires) is indexed by lat–lon.

### Bounding Boxes:
A rectange on earth defined by 4 numbers:
min_lat, max_lat
min_lon, max_lon

Bounding Boxes are used for:
- Download only required satellite images
- Filter AQ stations
- Filter fire points
- Speed up computations

### GeoJSON Basics:
A JSON file that stores geographic shapes.

It represents:
- Points (AQ stations)
- Lines (roads)
- Polygons (city boundaries)
- uses [long, lat] order

Its better than nounding boxes because
- It matches the exact city shape
- No extra area
- Enables accurate masking

We will use GeoJSON to:
- Clip satellite images
- Assign AQ stations to the city
- Create zones

### Grids/Zones(splitting a city into areas)
Instead of treating the city as one big unit, you divide it into smaller parts

Each zone has:
- Its own NDVI
- Its own PM2.5 trend
- Its own fire influence

