import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

def get_weather_ai_insight(city, temp, condition_code):
    """
    Uses AI to interpret weather data into actionable retail strategy.
    """
    # Retrieves key from environment variables (local .env or Streamlit Secrets)
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return " Error: OpenAI API Key not found in environment variables."

    client = OpenAI(api_key=api_key)
    
    # Context-rich prompt for specific retail impact
    prompt = f"""
    Act as a Retail Strategy Expert. 
    Location: {city}
    Current Temp: {temp}°C
    Weather Code: {condition_code} (WMO standard)

    Provide 2 brief, actionable points on how this specific weather 
    today affects customer foot traffic and delivery logistics in this area.
    Focus on practical business adjustments.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful retail consultant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7 # Adds a touch of creative strategy
        )
        return response.choices[0].message.content
    except Exception as e:
        # Returns a clean error message to the Streamlit UI
        return f"AI Insight unavailable: {str(e)}"