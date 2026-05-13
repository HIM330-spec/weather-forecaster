import streamlit as st
import pandas as pd
from main import get_coordinates, fetch_weather, fetch_forecast 
from analyzer import get_weather_ai_insight

# 1. Page Configuration
st.set_page_config(page_title="Global Weather Intelligence", page_icon="🌤️", layout="wide")

# 2. Business Logic Layer
def get_business_alerts(temp, rain_sum):
    alerts = []
    if temp > 35:
        alerts.append(" Extreme Heat: Expect reduced foot traffic. Promote delivery.")
    if rain_sum > 5:
        alerts.append(" Heavy Rain: Logistics delays likely. Check driver safety.")
    if 22 <= temp <= 28 and rain_sum < 1:
        alerts.append(" Optimal Conditions: High potential for foot traffic and outdoor sales.")
    return alerts

# 3. Session State Initialization (Search History)
if 'history' not in st.session_state:
    st.session_state.history = []

st.title(" Global Weather Intelligence")
st.markdown("Analyze real-time weather impacts on your business operations.")

# --- SIDEBAR: History & Quick Links ---
st.sidebar.subheader(" Recent Searches")
for loc in st.session_state.history[:5]:
    if st.sidebar.button(loc, use_container_width=True):
        # Splitting the saved string to pre-fill inputs
        parts = loc.split(", ")
        st.session_state['city_input'] = parts[0]
        st.session_state['state_input'] = parts[1]

# --- MAIN: Input Area ---
col1, col2, col3 = st.columns(3)
with col1:
    city = st.text_input("City", value=st.session_state.get('city_input', 'Ilorin'))
with col2:
    state = st.text_input("State", value=st.session_state.get('state_input', 'Kwara'))
with col3:
    country = st.text_input("Country", "Nigeria")

# --- EXECUTION ---
if st.button("Analyze Local Market", use_container_width=True):
    with st.spinner("Processing Market Data..."):
        lat, lon = get_coordinates(city, state, country)
        
        if lat and lon:
            # Update History
            loc_name = f"{city}, {state}"
            if loc_name not in st.session_state.history:
                st.session_state.history.insert(0, loc_name)

            # Fetch Current & Forecast Data
            weather = fetch_weather(lat, lon)
            forecast_data = fetch_forecast(lat, lon) # Needs to be defined in main.py
            
            if weather and forecast_data:
                temp = weather['temperature']
                
 # --- DISPLAY: Metrics ---
                st.divider()
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Current Temp", f"{temp}°C")
                m_col2.metric("Wind Speed", f"{weather['windspeed']} km/h")
                m_col3.metric("Predicted Rain", f"{forecast_data['precipitation_sum'][0]} mm")

# --- DISPLAY: Charts & Alerts ---
                tab1, tab2 = st.tabs([" 7-Day Trend", " Strategic Alerts"])
                
                with tab1:
                    chart_df = pd.DataFrame({
                        "Day": forecast_data['time'],
                        "Max Temp (°C)": forecast_data['temperature_2m_max'],
                        "Min Temp (°C)": forecast_data['temperature_2m_min']
                    }).set_index("Day")
                    st.line_chart(chart_df)

                with tab2:
                    alerts = get_business_alerts(temp, forecast_data['precipitation_sum'][0])
                    if alerts:
                        for a in alerts:
                            st.info(a)
                    else:
                        st.write("No critical weather alerts for today.")

# --- DISPLAY: AI Strategy ---
                st.subheader(" AI Business Strategy")
                insight = get_weather_ai_insight(city, temp, weather['weathercode'])
                st.markdown(insight)
            else:
                st.error("Failed to retrieve weather data.")
        else:
            st.error("Location not found. Please verify City and State names.")