# Smart Dashboard

Ein persönliches Streamlit-Dashboard, das Systemkennzahlen, Wetterdaten und einen Fokus-Timer kombiniert.

## Voraussetzungen
- Python 3.11 oder neuer
- [pip](https://pip.pypa.io/en/stable/getting-started/)

Installiere die Abhängigkeiten beispielsweise in einer virtuellen Umgebung:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Konfiguration
Lege eine `.env`-Datei an (oder setze die Variablen anderweitig), um den Wetterdienst zu konfigurieren:

```dotenv
OPENWEATHER_API_KEY=dein_api_key
CITY=Munich              # optional, Standard: Munich
COUNTRY_CODE=DE          # optional, Standard: DE
LANG=de                  # optional, Standard: de
UNITS=metric             # optional, Standard: metric
TIMEZONE=Europe/Berlin   # optional, Standard: Europe/Berlin
# LATITUDE=48.137
# LONGITUDE=11.575
```

Wenn `LATITUDE` und `LONGITUDE` gesetzt sind, werden die Koordinaten für die Abfrage verwendet.

## Starten

```bash
streamlit run dashboard.py --server.address 0.0.0.0 --server.port 8501
```

Öffne anschließend `http://<deine-ip>:8501` im Browser.
