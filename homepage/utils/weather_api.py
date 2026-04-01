import requests # type: ignore
from datetime import datetime

# Coordinates for major states and districts in India
INDIA_REGIONS = {
    "Andhra Pradesh": {
        "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185}, "Vijayawada": {"lat": 16.5062, "lon": 80.6480}, "Guntur": {"lat": 16.3067, "lon": 80.4365},
    },
    "Arunachal Pradesh": {"Itanagar": {"lat": 27.0844, "lon": 93.6053}},
    "Assam": {"Guwahati": {"lat": 26.1445, "lon": 91.7362}, "Dibrugarh": {"lat": 27.4728, "lon": 94.9120}},
    "Bihar": {"Patna": {"lat": 25.5941, "lon": 85.1376}, "Gaya": {"lat": 24.7914, "lon": 85.0002}},
    "Chhattisgarh": {"Raipur": {"lat": 21.2514, "lon": 81.6296}},
    "Goa": {"Panaji": {"lat": 15.4909, "lon": 73.8278}},
    "Gujarat": {"Ahmedabad": {"lat": 23.0225, "lon": 72.5714}, "Surat": {"lat": 21.1702, "lon": 72.8311}, "Rajkot": {"lat": 22.3039, "lon": 70.8022}},
    "Haryana": {"Chandigarh": {"lat": 30.7333, "lon": 76.7794}, "Faridabad": {"lat": 28.4089, "lon": 77.3178}},
    "Himachal Pradesh": {"Shimla": {"lat": 31.1048, "lon": 77.1734}},
    "Jharkhand": {"Ranchi": {"lat": 23.3441, "lon": 85.3096}},
    "Karnataka": {"Bengaluru": {"lat": 12.9716, "lon": 77.5946}, "Mysuru": {"lat": 12.2958, "lon": 76.6394}, "Hubballi": {"lat": 15.3647, "lon": 75.1240}},
    "Kerala": {"Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366}, "Kochi": {"lat": 9.9312, "lon": 76.2673}, "Kozhikode": {"lat": 11.2588, "lon": 75.7804}},
    "Madhya Pradesh": {"Bhopal": {"lat": 23.2599, "lon": 77.4126}, "Indore": {"lat": 22.7196, "lon": 75.8577}},
    "Maharashtra": {"Mumbai": {"lat": 19.0760, "lon": 72.8777}, "Pune": {"lat": 18.5204, "lon": 73.8567}, "Nagpur": {"lat": 21.1458, "lon": 79.0882}, "Nashik": {"lat": 20.0110, "lon": 73.7903}},
    "Manipur": {"Imphal": {"lat": 24.8170, "lon": 93.9368}},
    "Meghalaya": {"Shillong": {"lat": 25.5788, "lon": 91.8933}},
    "Mizoram": {"Aizawl": {"lat": 23.7271, "lon": 92.7176}},
    "Nagaland": {"Kohima": {"lat": 25.6751, "lon": 94.1086}},
    "Odisha": {"Bhubaneswar": {"lat": 20.2961, "lon": 85.8245}, "Cuttack": {"lat": 20.4625, "lon": 85.8828}},
    "Punjab": {"Ludhiana": {"lat": 30.9010, "lon": 75.8573}, "Amritsar": {"lat": 31.6340, "lon": 74.8723}, "Jalandhar": {"lat": 31.3260, "lon": 75.5762}},
    "Rajasthan": {"Jaipur": {"lat": 26.9124, "lon": 75.7873}, "Jodhpur": {"lat": 26.2389, "lon": 73.0243}},
    "Sikkim": {"Gangtok": {"lat": 27.3314, "lon": 88.6138}},
    "Tamil Nadu": {
        "Chennai": {"lat": 13.0827, "lon": 80.2707}, "Coimbatore": {"lat": 11.0168, "lon": 76.9558}, "Madurai": {"lat": 9.9252, "lon": 78.1198},
        "Tiruchirappalli": {"lat": 10.7905, "lon": 78.7047}, "Salem": {"lat": 11.6643, "lon": 78.1460}, "Tirunelveli": {"lat": 8.7139, "lon": 77.7567},
        "Erode": {"lat": 11.3410, "lon": 77.7172}, "Vellore": {"lat": 12.9165, "lon": 79.1325}, "Thoothukudi": {"lat": 8.7642, "lon": 78.1348},
        "Dindigul": {"lat": 10.3673, "lon": 77.9803}, "Thanjavur": {"lat": 10.7870, "lon": 79.1378}, "Kanyakumari": {"lat": 8.0883, "lon": 77.5385}
    },
    "Telangana": {"Hyderabad": {"lat": 17.3850, "lon": 78.4867}, "Warangal": {"lat": 17.9689, "lon": 79.5941}},
    "Tripura": {"Agartala": {"lat": 23.8315, "lon": 91.2868}},
    "Uttar Pradesh": {"Lucknow": {"lat": 26.8467, "lon": 80.9462}, "Kanpur": {"lat": 26.4499, "lon": 80.3319}, "Agra": {"lat": 27.1767, "lon": 78.0081}, "Varanasi": {"lat": 25.3176, "lon": 83.0060}},
    "Uttarakhand": {"Dehradun": {"lat": 30.3165, "lon": 78.0322}},
    "West Bengal": {"Kolkata": {"lat": 22.5726, "lon": 88.3639}, "Siliguri": {"lat": 26.7271, "lon": 88.3953}, "Darjeeling": {"lat": 27.0360, "lon": 88.2636}}
}

def get_realtime_weather():
    """Returns empty as we now require a specific state and district."""
    return []

def get_dashboard_weather():
    """Fetches real-time weather based on public IP location, with fallback to Pune."""
    try:
        # Get location from public IP
        ip_response = requests.get('https://ipapi.co/json/', timeout=5)
        if ip_response.status_code == 200:
            ip_data = ip_response.json()
            lat = ip_data.get('latitude')
            lon = ip_data.get('longitude')
            city = ip_data.get('city', 'Unknown')
            
            if lat is not None and lon is not None:
                weather = _fetch_weather_from_coords(lat, lon, city)
                if weather:
                    return weather
    except Exception as e:
        print(f"Error fetching IP location for dashboard weather: {e}")
        
    # Using Pune as a fallback agricultural proxy if IP location fails or isn't available
    weather_data = get_realtime_weather_for_district("Maharashtra", "Pune")
    if weather_data and not weather_data[0].get('error'):
        return weather_data[0]
    return None

def _fetch_weather_from_coords(lat, lon, city):
    """Helper to fetch weather directly from coordinates."""
    try:
        tz_encoded = "Asia%2FKolkata"
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
            f"&timezone={tz_encoded}"
        )
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            return {
                "city": city,
                "temperature": current.get("temperature_2m", "--"),
                "humidity": current.get("relative_humidity_2m", "--"),
                "rainfall": current.get("precipitation", "--"),
                "wind_speed": current.get("wind_speed_10m", "--"),
                "time": current.get("time", "").replace("T", " ")
            }
    except Exception as e:
        print(f"Error fetching weather for coords {lat},{lon}: {e}")
    return None

def get_realtime_weather_for_district(state, district):
    """Fetches real-time weather for a single specific district within a state."""
    if state not in INDIA_REGIONS or district not in INDIA_REGIONS[state]:
        return [_get_fallback_data(district)]
    
    coords = INDIA_REGIONS[state][district]
    try:
        tz_encoded = "Asia%2FKolkata"

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={coords['lat']}&longitude={coords['lon']}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
            f"&timezone={tz_encoded}"
        )
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            return [{
                "city": district,
                "temperature": current.get("temperature_2m", "--"),
                "humidity": current.get("relative_humidity_2m", "--"),
                "rainfall": current.get("precipitation", "--"),
                "wind_speed": current.get("wind_speed_10m", "--"),
                "time": current.get("time", "").replace("T", " ")
            }]
        else:
            return [_get_fallback_data(district)]
    except Exception as e:
        print(f"Error fetching weather for {district}: {e}")
        return [_get_fallback_data(district)]

def _get_fallback_data(city):
    """Fallback data in case the API fails or is unreachable."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "city": city,
        "temperature": "N/A",
        "humidity": "N/A",
        "rainfall": "N/A",
        "wind_speed": "N/A",
        "time": current_time,
        "error": True
    }
