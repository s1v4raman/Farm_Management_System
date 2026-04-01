import requests

# Test geocoding
city = "Coimbatore"
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
res = requests.get(geo_url).json()

print("Geocoding Response:")
print(res)

if "results" in res and len(res["results"]) > 0:
    lat = res["results"][0]["latitude"]
    lon = res["results"][0]["longitude"]
    
    # Test weather with daily forecast
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max&timezone=auto&past_days=1&forecast_days=6"
    
    w_res = requests.get(weather_url).json()
    print("Weather Response:")
    print(w_res)
