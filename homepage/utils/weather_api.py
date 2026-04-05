import requests # type: ignore
from datetime import datetime

# Coordinates for major states and districts in India
INDIA_STATES = {
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
    "Meghalaya": {
        "Shillong": {"lat": 25.5788, "lon": 91.8933},
        "Tura": {"lat": 25.5141, "lon": 90.2201},
        "Jowai": {"lat": 25.4484, "lon": 92.2035},
        "Nongstoin": {"lat": 25.5192, "lon": 91.2694},
        "Nongpoh": {"lat": 25.9015, "lon": 91.8804},
        "Khliehriat": {"lat": 25.3578, "lon": 92.3686},
        "Williamnagar": {"lat": 25.4965, "lon": 90.5833},
        "Resubelpara": {"lat": 25.9100, "lon": 90.6125},
        "Mawkyrwat": {"lat": 25.3653, "lon": 91.2651},
        "Mairang": {"lat": 25.5683, "lon": 91.6366},
        "Baghmara": {"lat": 25.2152, "lon": 90.6416},
        "Ampati": {"lat": 25.3900, "lon": 89.9325},
    },
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

USA_STATES = {
    "California": {"Los Angeles": {"lat": 34.0522, "lon": -118.2437}, "San Francisco": {"lat": 37.7749, "lon": -122.4194}, "Fresno": {"lat": 36.7378, "lon": -119.7871}, "Sacramento": {"lat": 38.5816, "lon": -121.4944}, "San Diego": {"lat": 32.7157, "lon": -117.1611}},
    "Texas": {"Houston": {"lat": 29.7604, "lon": -95.3698}, "Austin": {"lat": 30.2672, "lon": -97.7431}, "Dallas": {"lat": 32.7767, "lon": -96.7970}, "San Antonio": {"lat": 29.4241, "lon": -98.4936}, "El Paso": {"lat": 31.7619, "lon": -106.4850}},
    "Florida": {"Miami": {"lat": 25.7617, "lon": -80.1918}, "Orlando": {"lat": 28.5383, "lon": -81.3792}, "Tampa": {"lat": 27.9506, "lon": -82.4572}, "Jacksonville": {"lat": 30.3322, "lon": -81.6557}},
    "New York": {"New York City": {"lat": 40.7128, "lon": -74.0060}, "Buffalo": {"lat": 42.8864, "lon": -78.8784}, "Rochester": {"lat": 43.1566, "lon": -77.6088}},
    "Illinois": {"Chicago": {"lat": 41.8781, "lon": -87.6298}, "Springfield": {"lat": 39.7817, "lon": -89.6501}},
    "Washington": {"Seattle": {"lat": 47.6062, "lon": -122.3321}, "Spokane": {"lat": 47.6588, "lon": -117.4260}},
}

UK_STATES = {
    "England": {"London": {"lat": 51.5074, "lon": -0.1278}, "Manchester": {"lat": 53.4808, "lon": -2.2426}, "Birmingham": {"lat": 52.4862, "lon": -1.8904}, "Liverpool": {"lat": 53.4084, "lon": -2.9916}, "Leeds": {"lat": 53.8008, "lon": -1.5491}},
    "Scotland": {"Edinburgh": {"lat": 55.9533, "lon": -3.1883}, "Glasgow": {"lat": 55.8642, "lon": -4.2518}, "Aberdeen": {"lat": 57.1497, "lon": -2.0943}},
    "Wales": {"Cardiff": {"lat": 51.4816, "lon": -3.1791}, "Swansea": {"lat": 51.6214, "lon": -3.9436}, "Newport": {"lat": 51.5842, "lon": -2.9977}},
    "Northern Ireland": {"Belfast": {"lat": 54.5973, "lon": -5.9301}, "Derry": {"lat": 55.0068, "lon": -7.3183}},
}

AUSTRALIA_STATES = {
    "New South Wales": {"Sydney": {"lat": -33.8688, "lon": 151.2093}, "Newcastle": {"lat": -32.9283, "lon": 151.7817}, "Wollongong": {"lat": -34.4278, "lon": 150.8931}},
    "Victoria": {"Melbourne": {"lat": -37.8136, "lon": 144.9631}, "Geelong": {"lat": -38.1499, "lon": 144.3617}, "Ballarat": {"lat": -37.5622, "lon": 143.8503}},
    "Queensland": {"Brisbane": {"lat": -27.4698, "lon": 153.0251}, "Gold Coast": {"lat": -28.0167, "lon": 153.4000}, "Cairns": {"lat": -16.9186, "lon": 145.7781}},
    "Western Australia": {"Perth": {"lat": -31.9505, "lon": 115.8605}, "Fremantle": {"lat": -32.0569, "lon": 115.7439}},
    "South Australia": {"Adelaide": {"lat": -34.9285, "lon": 138.6007}, "Mount Gambier": {"lat": -37.8284, "lon": 140.7804}},
}

CANADA_STATES = {
    "Ontario": {"Toronto": {"lat": 43.6532, "lon": -79.3832}, "Ottawa": {"lat": 45.4215, "lon": -75.6972}},
    "British Columbia": {"Vancouver": {"lat": 49.2827, "lon": -123.1207}, "Victoria": {"lat": 48.4284, "lon": -123.3656}},
    "Quebec": {"Montreal": {"lat": 45.5017, "lon": -73.5673}, "Quebec City": {"lat": 46.8139, "lon": -71.2080}}
}

GERMANY_STATES = {
    "Bavaria": {"Munich": {"lat": 48.1351, "lon": 11.5820}, "Nuremberg": {"lat": 49.4521, "lon": 11.0767}},
    "Berlin": {"Berlin": {"lat": 52.5200, "lon": 13.4050}},
    "Hesse": {"Frankfurt": {"lat": 50.1109, "lon": 8.6821}}
}

FRANCE_STATES = {
    "Île-de-France": {"Paris": {"lat": 48.8566, "lon": 2.3522}},
    "Provence-Alpes-Côte d'Azur": {"Marseille": {"lat": 43.2965, "lon": 5.3698}, "Nice": {"lat": 43.7102, "lon": 7.2620}},
    "Auvergne-Rhône-Alpes": {"Lyon": {"lat": 45.7640, "lon": 4.8357}}
}

JAPAN_STATES = {
    "Tokyo": {"Tokyo": {"lat": 35.6895, "lon": 139.6917}},
    "Osaka": {"Osaka": {"lat": 34.6937, "lon": 135.5023}},
    "Hokkaido": {"Sapporo": {"lat": 43.0618, "lon": 141.3545}}
}

BRAZIL_STATES = {
    "São Paulo": {"São Paulo": {"lat": -23.5505, "lon": -46.6333}},
    "Rio de Janeiro": {"Rio de Janeiro": {"lat": -22.9068, "lon": -43.1729}},
    "Federal District": {"Brasília": {"lat": -15.7975, "lon": -47.8919}}
}

WORLD_REGIONS = {
    "India": INDIA_STATES,
    "United States": USA_STATES,
    "United Kingdom": UK_STATES,
    "Australia": AUSTRALIA_STATES,
    "Canada": CANADA_STATES,
    "Germany": GERMANY_STATES,
    "France": FRANCE_STATES,
    "Japan": JAPAN_STATES,
    "Brazil": BRAZIL_STATES,
    "China": {
        "Beijing": {"Beijing": {"lat": 39.9042, "lon": 116.4074}},
        "Shanghai": {"Shanghai": {"lat": 31.2304, "lon": 121.4737}},
        "Guangdong": {"Guangzhou": {"lat": 23.1291, "lon": 113.2644}, "Shenzhen": {"lat": 22.5431, "lon": 114.0579}}
    },
    "Russia": {
        "Moscow": {"Moscow": {"lat": 55.7558, "lon": 37.6173}},
        "Saint Petersburg": {"Saint Petersburg": {"lat": 59.9343, "lon": 30.3351}}
    },
    "South Africa": {
        "Gauteng": {"Johannesburg": {"lat": -26.2041, "lon": 28.0473}, "Pretoria": {"lat": -25.7479, "lon": 28.2293}},
        "Western Cape": {"Cape Town": {"lat": -33.9249, "lon": 18.4241}}
    },
    "Italy": {
        "Lazio": {"Rome": {"lat": 41.9028, "lon": 12.4964}},
        "Lombardy": {"Milan": {"lat": 45.4642, "lon": 9.1900}},
        "Tuscany": {"Florence": {"lat": 43.7696, "lon": 11.2558}}
    },
    "Spain": {
        "Madrid": {"Madrid": {"lat": 40.4168, "lon": -3.7038}},
        "Catalonia": {"Barcelona": {"lat": 41.3851, "lon": 2.1734}}
    },
    "Mexico": {
        "Mexico City": {"Mexico City": {"lat": 19.4326, "lon": -99.1332}},
        "Jalisco": {"Guadalajara": {"lat": 20.6597, "lon": -103.3496}}
    }
}


def get_realtime_weather():
    """Returns empty as we now require a specific state and district."""
    return []

def get_dashboard_weather(ip_address=None):
    """Fetches real-time weather based on public IP location, with fallback to Pune."""
    # Try ipapi.co first
    try:
        url = 'https://ipapi.co/json/'
        if ip_address and ip_address != '127.0.0.1':
            url = f'https://ipapi.co/{ip_address}/json/'
            
        ip_response = requests.get(url, timeout=3)
        if ip_response.status_code == 200:
            ip_data = ip_response.json()
            lat, lon = ip_data.get('latitude'), ip_data.get('longitude')
            city = ip_data.get('city', 'Unknown')
            if lat is not None and lon is not None:
                weather = _fetch_weather_from_coords(lat, lon, city)
                if weather: return weather
    except Exception: pass

    # Backup: Try ipwhois.app
    try:
        url = 'https://ipwho.is/'
        if ip_address and ip_address != '127.0.0.1':
            url = f'https://ipwho.is/{ip_address}'
            
        ip_response = requests.get(url, timeout=3)
        if ip_response.status_code == 200:
            ip_data = ip_response.json()
            if ip_data.get('success'):
                lat, lon = ip_data.get('latitude'), ip_data.get('longitude')
                city = ip_data.get('city', 'Unknown')
                weather = _fetch_weather_from_coords(lat, lon, city)
                if weather: return weather
    except Exception: pass
        
    # Using Pune as a fallback agricultural proxy if IP location fails or isn't available
    weather_data = get_realtime_weather_for_district("India", "Maharashtra", "Pune")
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
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            return {
                "city": city,
                "temperature": current.get("temperature_2m", 0),
                "humidity": current.get("relative_humidity_2m", 0),
                "rainfall": current.get("precipitation", 0),
                "wind_speed": current.get("wind_speed_10m", 0),
                "time": current.get("time", "").replace("T", " ")
            }
    except Exception:
        pass
    return None

def get_realtime_weather_for_district(country, state, district):
    """Fetches real-time weather for a single specific district within a state/country."""
    if country not in WORLD_REGIONS or state not in WORLD_REGIONS[country] or district not in WORLD_REGIONS[country][state]:
        return [_get_fallback_data(district)]
    
    coords = WORLD_REGIONS[country][state][district]
    try:
        tz_encoded = "Asia%2FKolkata"
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={coords['lat']}&longitude={coords['lon']}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
            f"&timezone={tz_encoded}"
        )
        
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            return [{
                "city": district,
                "temperature": current.get("temperature_2m", 0),
                "humidity": current.get("relative_humidity_2m", 0),
                "rainfall": current.get("precipitation", 0),
                "wind_speed": current.get("wind_speed_10m", 0),
                "time": current.get("time", "").replace("T", " ")
            }]
    except Exception:
        pass
    return [_get_fallback_data(district)]

def get_7_day_weather_forecast(country, state, district):
    """
    Fetches the 7-day weather forecast (1 past, 1 present, 5 future) for a given district.
    Uses Open-Meteo geocoding to dynamically find coordinates.
    """
    try:
        # Step 1: Geocode the location
        # Using district name to find coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={district}&count=10&language=en&format=json"
        geo_res = requests.get(geo_url, timeout=5)
        
        if geo_res.status_code != 200:
            return None
            
        geo_data = geo_res.json()
        if not geo_data.get("results"):
            # If district fails, try state
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={state}&count=5&language=en&format=json"
            geo_data = requests.get(geo_url, timeout=5).json()
            if not geo_data.get("results"):
                return None
                
        results = geo_data["results"]
        # Find best match. If country is provided and not "Global", try to match it.
        best_match = results[0]
        if country and country.lower() != "global":
            for r in results:
                if r.get("country", "").lower() == country.lower():
                    best_match = r
                    break
                
        lat = best_match["latitude"]
        lon = best_match["longitude"]
        resolved_city = best_match.get("name", district)
        resolved_state = best_match.get("admin1", state)
        resolved_country = best_match.get("country", country)

        # Step 2: Fetch 7-day forecast (past_days=1, forecast_days=6 equals 7 days total including today)
        tz_encoded = "auto"
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,uv_index_max"
            f"&timezone={tz_encoded}"
            f"&past_days=1&forecast_days=6"
        )
        
        weather_res = requests.get(weather_url, timeout=5)
        if weather_res.status_code != 200:
            return None
            
        weather_data = weather_res.json()
        current = weather_data.get("current", {})
        daily = weather_data.get("daily", {})
        
        # Build response object
        response = {
            "city": resolved_city,
            "current": {
                "temperature": current.get("temperature_2m", "--"),
                "humidity": current.get("relative_humidity_2m", "--"),
                "rainfall": current.get("precipitation", "--"),
                "wind_speed": current.get("wind_speed_10m", "--"),
                "time": current.get("time", "").replace("T", " ")
            },
            "daily": []
        }
        
        # Process the 7 days (index 0 is yesterday, index 1 is today, 2-6 are future)
        times = daily.get("time", [])
        for i in range(len(times)):
            day_type = "Future"
            if i == 0:
                day_type = "Previous Day"
            elif i == 1:
                day_type = "Present Day"
                
            # Parse date to weekday
            date_obj = datetime.strptime(times[i], "%Y-%m-%d")
            weekday = date_obj.strftime("%A")
                
            response["daily"].append({
                "date": times[i],
                "weekday": weekday,
                "day_type": day_type,
                "temp_max": daily.get("temperature_2m_max", [])[i],
                "temp_min": daily.get("temperature_2m_min", [])[i],
                "rainfall": daily.get("precipitation_sum", [])[i],
                "wind_speed_max": daily.get("wind_speed_10m_max", [])[i],
            })
            
        return response
    except Exception as e:
        print(f"Error fetching 7-day forecast API: {e}")
        return None

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
