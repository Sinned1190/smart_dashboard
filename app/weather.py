import os
import requests

class WeatherError(Exception):
    pass

def load_weather_config():
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    city = os.getenv("CITY", "Munich").strip()
    country = os.getenv("COUNTRY_CODE", "DE").strip()
    lang = os.getenv("LANG", "de").strip()
    units = os.getenv("UNITS", "metric").strip()
    timezone = os.getenv("TIMEZONE", "Europe/Berlin").strip()

    if not api_key:
        raise WeatherError("OPENWEATHER_API_KEY fehlt. Bitte in der .env Datei setzen.")
    return api_key, city, country, lang, units, timezone

def fetch_current_weather(api_key: str, city: str, country: str, lang: str, units: str, timezone: str) -> dict:
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    q = f"{city},{country}",
    params = {"q": q, "appid": api_key, "lang": lang, "units": units, "tz": timezone}

    resp = requests.get(base_url, params=params, timeout=10)
    if resp.status_code != 200:
        raise WeatherError(f"Fehler beim Abrufen der Wetterdaten: {resp.status_code} - {resp.text}")
    
    data = resp.json()

    weather = {
        "location": f"{data.get('name', city)}, {country}",
        "description": (data.get("weather", [{}])[0].get("description", "Keine Daten")).capitalize(),
        "temperature": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "icon": data.get("weather", [{}])[0].get("icon"),
    }
    return weather

