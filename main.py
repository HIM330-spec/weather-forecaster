import requests

def get_coordinates(city, state, country):
    """Converts location names into Latitude/Longitude using Nominatim."""
    query = f"{city}, {state}, {country}"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    headers = {'User-Agent': 'SalesIntelApp/1.0'} # Required for OSM compliance
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None

def fetch_weather(lat, lon):
    """Fetches real-time weather from Open-Meteo."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data.get('current_weather')
    except Exception as e:
        print(f"Weather fetch error: {e}")
        return None
