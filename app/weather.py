"""Utilities for loading and retrieving weather information."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import requests


class WeatherError(Exception):
    """Raised when weather data cannot be loaded or parsed."""


@dataclass(frozen=True)
class WeatherConfig:
    api_key: str
    city: str
    country: str
    lang: str
    units: str
    timezone: str
    latitude: Optional[float]
    longitude: Optional[float]


def _read_float_env(name: str) -> Optional[float]:
    """Return the environment value as float if present, otherwise ``None``."""

    raw = os.getenv(name, "").strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError as exc:  # pragma: no cover - defensive coding
        raise WeatherError(f"{name} muss eine Zahl sein (z. B. 48.137).") from exc


def _resolve_timezone(name: str) -> ZoneInfo:
    """Resolve a timezone name to a ``ZoneInfo`` instance."""

    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise WeatherError(f"Unbekannte Zeitzone '{name}'.") from exc


def load_weather_config() -> WeatherConfig:
    """Load and validate configuration for the weather request."""

    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    city = os.getenv("CITY", "Munich").strip()
    country = os.getenv("COUNTRY_CODE", "DE").strip()
    lang = os.getenv("LANG", "de").strip()
    units = os.getenv("UNITS", "metric").strip()
    timezone = os.getenv("TIMEZONE", "Europe/Berlin").strip()
    latitude = _read_float_env("LATITUDE")
    longitude = _read_float_env("LONGITUDE")

    if not api_key:
        raise WeatherError("OPENWEATHER_API_KEY fehlt. Bitte in der .env Datei setzen.")

    if (latitude is None) != (longitude is None):
        raise WeatherError("LATITUDE und LONGITUDE müssen gemeinsam gesetzt werden.")

    # Validate timezone early to surface misconfiguration.
    _resolve_timezone(timezone)

    return WeatherConfig(
        api_key=api_key,
        city=city,
        country=country,
        lang=lang,
        units=units,
        timezone=timezone,
        latitude=latitude,
        longitude=longitude,
    )


def fetch_current_weather(config: WeatherConfig) -> Dict[str, Any]:
    """Fetch current weather information from OpenWeather."""

    params: Dict[str, Any] = {
        "appid": config.api_key,
        "lang": config.lang,
        "units": config.units,
    }

    if config.latitude is not None and config.longitude is not None:
        params.update({"lat": config.latitude, "lon": config.longitude})
    else:
        params["q"] = f"{config.city},{config.country}"

    try:
        resp = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise WeatherError(f"Fehler beim Abrufen der Wetterdaten: {exc}") from exc

    data = resp.json()

    tz = _resolve_timezone(config.timezone)
    observation_ts = data.get("dt")
    observed_at = datetime.fromtimestamp(observation_ts, tz) if observation_ts else datetime.now(tz)

    weather = {
        "location": f"{data.get('name', config.city)}, {config.country}",
        "description": (data.get("weather", [{}])[0].get("description") or "Keine Daten").capitalize(),
        "temperature": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "pressure": data.get("main", {}).get("pressure"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "visibility": data.get("visibility"),
        "icon": data.get("weather", [{}])[0].get("icon"),
        "observed_at": observed_at,
    }

    return weather

