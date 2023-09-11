from geopy.geocoders import Nominatim
import pandas as pd

path = '/air_quality_data.csv'
df = pd.read_csv(path)

unique_cities = df['City'].unique()
print("Number of unique cities:", len(unique_cities))

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="city_locator")

city_data = []

for city in unique_cities:
    location = geolocator.geocode(city + ', India')
    if location is not None:
        print(city, location.latitude, location.longitude)
        city_data.append({
            'City': city,
            'Latitude': location.latitude,
            'Longitude': location.longitude
        })

city_df = pd.DataFrame(city_data)
city_df.to_csv('city_coordinates.csv', index=False)