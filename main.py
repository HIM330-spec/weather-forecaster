import requests

def get_coordinates(city, state, country):
    """
    Converts location names into Latitude/Longitude using Nominatim.
    """
    query = f"{city}, {state}, {country}"
    url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
    # User-Agent is mandatory for Nominatim to avoid 403 Forbidden errors
    headers = {'User-Agent': 'WeatherIntelApp/1.0'} 
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None

def fetch_weather(lat, lon):
    """
    Fetches real-time current weather data.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('current_weather')
    except Exception as e:
        print(f"Weather fetch error: {e}")
        return None

def fetch_forecast(lat, lon):
    """
    Fetches a 7-day daily forecast outlook.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get('daily')
    except Exception as e:
        print(f"Forecast fetch error: {e}")
        return None

def get_business_alerts(temp, rain_sum):
    """
    Translates environmental data into actionable business warnings.
    """
    alerts = []
    
    # Heat Alert
    if temp > 35:
        alerts.append(" **Extreme Heat:** Expect reduced foot traffic. Suggest promoting delivery services.")
    
    # Rain Alert
    if rain_sum > 5:
        alerts.append(" **Heavy Rain Predicted:** Logistics and dispatch delays likely. Advise riders to take extra caution.")
    
    # Optimal Conditions
    if 20 <= temp <= 28 and rain_sum < 1:
        alerts.append(" **Ideal Market Conditions:** Great weather for outdoor activations and increased walk-in customers.")
        
    # Cold/Storm Alert (Optional addition for completeness)
    if temp < 15:
        alerts.append(" **Cooler Temperatures:** Potential increase in demand for hot beverages or indoor-focused services.")
        
    return alerts