import streamlit as st
import pandas as pd
from main import get_coordinates, fetch_weather
from analyzer import get_weather_ai_insight

st.set_page_config(page_title="Global Weather Intelligence", page_icon="🌤️")

st.title("🌤️ Global Weather Intelligence")
st.markdown("Enter a location to get real-time weather and business impact analysis.")

# --- Layout: Main Input Area ---
# Using columns to organize the input fields horizontally
col1, col2, col3 = st.columns(3)

with col1:
    city = st.text_input("City", "Ilorin")
with col2:
    state = st.text_input("State", "Kwara")
with col3:
    country = st.text_input("Country", "Nigeria")

# Centered button
if st.button("Analyze Local Weather", use_container_width=True):
    with st.spinner("Locating and fetching data..."):
        lat, lon = get_coordinates(city, state, country)
        
        if lat and lon:
            weather = fetch_weather(lat, lon)
            if weather:
                temp = weather['temperature']
                wind = weather['windspeed']
                
                st.divider()
                
                # --- Layout: Results Display ---
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric(label=f"Temperature in {city}", value=f"{temp}°C")
                with res_col2:
                    st.metric(label="Wind Speed", value=f"{wind} km/h")
                
                # --- AI Strategy Section ---
                st.subheader("🤖 AI Business Strategy")
                insight = get_weather_ai_insight(city, temp, weather['weathercode'])
                st.write(insight)
                st.info(f"The current weather in {city} is being analyzed.")
                
            else:
                st.error("Weather data currently unavailable.")
        else:
            st.error("Location not found. Please check your spelling.")
