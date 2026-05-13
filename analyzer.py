import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_weather_ai_insight(city, temp, condition_code):
    """AI interprets weather impact on local business."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    Act as a Retail Strategy Expert. 
    Location: {city}
    Current Temp: {temp}°C
    Weather Code: {condition_code} (WMO standard)

    Provide 2 brief, actionable points on how this specific weather 
    today affects customer foot traffic and delivery logistics in this area.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Insight unavailable: {e}"