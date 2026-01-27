import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load your CSV
df = pd.read_csv("data/raw/air_quality/stations_info.csv")

# Initialize geocoder
geolocator = Nominatim(user_agent="delhi_air_quality_mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Function to get lat/long
def get_lat_long(row):
    query = f"{row['station_location']}, {row['city']}, {row['state']}, India"
    location = geocode(query)
    if location:
        return pd.Series([location.latitude, location.longitude])
    return pd.Series([None, None])

# Apply geocoding
df[["latitude", "longitude"]] = df.apply(get_lat_long, axis=1)

# Save output
df.to_csv("data/processed/stations_with_lat_long.csv", index=False)

print("✅ Geocoding complete. Saved as stations_with_lat_long.csv")
