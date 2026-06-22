from flask import Flask, render_template, jsonify
import urllib.request
import json
import time
from datetime import datetime

app = Flask(__name__)

CITIES = {
    "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185},
    "Vijayawada":    {"lat": 16.5062, "lon": 80.6480},
    "Tirupati":      {"lat": 13.6288, "lon": 79.4192},
    "Hyderabad":     {"lat": 17.3850, "lon": 78.4867},
}

def fetch_weather(city, coords):
    """Fetch live weather from Open-Meteo API (no API key required)."""
    lat, lon = coords["lat"], coords["lon"]
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation,weather_code,wind_speed_10m,wind_direction_10m,"
        f"surface_pressure,visibility,uv_index"
        f"&wind_speed_unit=kmh"
        f"&timezone=Asia%2FKolkata"
    )
    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            data = json.loads(resp.read())
        c = data["current"]
        return {
            "city": city,
            "temperature":    round(c["temperature_2m"], 1),
            "feels_like":     round(c["apparent_temperature"], 1),
            "humidity":       c["relative_humidity_2m"],
            "precipitation":  c["precipitation"],
            "wind_speed":     round(c["wind_speed_10m"], 1),
            "wind_direction": c["wind_direction_10m"],
            "pressure":       round(c["surface_pressure"], 1),
            "visibility":     round(c.get("visibility", 0) / 1000, 1),
            "uv_index":       c.get("uv_index", 0),
            "weather_code":   c["weather_code"],
            "description":    weather_description(c["weather_code"]),
            "icon":           weather_icon(c["weather_code"]),
            "is_raining":     is_raining(c["weather_code"]),
            "updated":        datetime.now().strftime("%H:%M:%S IST"),
            "error":          None,
        }
    except Exception as e:
        return {"city": city, "error": str(e)}


def weather_description(code):
    mapping = {
        0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
        45: "Foggy", 48: "Icy Fog",
        51: "Light Drizzle", 53: "Moderate Drizzle", 55: "Heavy Drizzle",
        61: "Light Rain", 63: "Moderate Rain", 65: "Heavy Rain",
        71: "Light Snow", 73: "Moderate Snow", 75: "Heavy Snow",
        80: "Light Showers", 81: "Moderate Showers", 82: "Heavy Showers",
        95: "Thunderstorm", 96: "Thunderstorm w/ Hail", 99: "Severe Thunderstorm",
    }
    return mapping.get(code, "Unknown")


def weather_icon(code):
    """Return an emoji icon; rain codes get distinct icons by intensity."""
    if code == 0:            return "☀️"
    elif code in (1, 2):     return "🌤️"
    elif code == 3:          return "☁️"
    elif code in (45, 48):   return "🌫️"
    # Drizzle — light to heavy
    elif code == 51:         return "🌦️"   # light drizzle
    elif code == 53:         return "🌧️"   # moderate drizzle
    elif code == 55:         return "🌧️"   # heavy drizzle
    # Rain — light / moderate / heavy
    elif code == 61:         return "🌦️"   # light rain
    elif code == 63:         return "🌧️"   # moderate rain
    elif code == 65:         return "🌊"   # heavy rain
    # Freezing rain
    elif code in (66, 67):   return "🌨️"
    # Snow
    elif code in range(71, 78): return "❄️"
    # Rain showers — light / moderate / violent
    elif code == 80:         return "🌦️"   # light showers
    elif code == 81:         return "🌧️"   # moderate showers
    elif code == 82:         return "⛈️"   # violent showers
    # Thunderstorm
    elif code in (95, 96, 99): return "⛈️"
    return "🌡️"


def is_raining(code):
    """Return True for any precipitation weather code."""
    rain_codes = {51,53,55,56,57,61,63,65,66,67,80,81,82,95,96,99}
    return code in rain_codes


@app.route("/")
def index():
    return render_template("index.html", cities=list(CITIES.keys()))


@app.route("/api/weather")
def api_weather():
    results = []
    for city, coords in CITIES.items():
        results.append(fetch_weather(city, coords))
        time.sleep(0.1)          # be polite to the free API
    return jsonify(results)


@app.route("/api/weather/<city_name>")
def api_weather_city(city_name):
    city = next((c for c in CITIES if c.lower() == city_name.lower()), None)
    if not city:
        return jsonify({"error": "City not found"}), 404
    return jsonify(fetch_weather(city, CITIES[city]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
