# Sensor-driven Website (M5Stick TVOC/eCO₂ logger)

A simple IoT web application that collects TVOC and eCO₂ measurements from an M5Stick device and shows them on a server-rendered website. The device posts measurements to the server once per minute and the server validates and stores them in a local SQLite database and serves two HTML pages: a front page with the latest + min/max values and a measurements page with all recorded data.

This is a project from the 2. semester course 'The Web of Things' at Aarhus University. The goal of the project was to get a general understanding of the technologies in the best case scenario. Therefore testing, error handling and security is simple or non-existing.

<img width="416" height="549" alt="Skærmbillede (30)" src="https://github.com/user-attachments/assets/42bceb0b-13a1-4c68-9ad8-ebda82f72fb8" />
<img width="1312" height="649" alt="image" src="https://github.com/user-attachments/assets/2da03987-571f-4e6a-a98e-e35c54fd7e28" />

---

Project summary
---------------
- Device: M5Stick (UIFlow) with gas sensor (TVOC and eCO₂) + PIR for display control.
- Device behavior: reads sensor once per minute, shows latest and local min/max on device, uses PIR to toggle backlight, and posts measurements to the server via HTTP.
- Server: Flask app that accepts device measurements, stores validated readings in an SQLite database, and serves two HTML pages (front page and measurements page).
- Browser/Remote+: Front page auto-refreshes once per minute and shows latest/min/max; measurements page lists all entries.

Repository structure (key files)
-------------------------------
- main.py — Flask app (routes, API endpoint, DB connection management)
- db_handler.py — MeasurementsDB class: manages SQLite connection, table creation, insertion, queries
- templates/
  - base.html — base Jinja template
  - home.html — front page (latest, min, max; references static/js/home.js)
  - measurements.html — page listing all measurements
- static/js/home.js — front-page client script; polls the server (GET /updateMeasurements) every 60s and updates the DOM

API (endpoints and payloads)
----------------------------
- GET / or /home
  - Renders the front page (templates/home.html). The front page loads static/js/home.js which itself calls GET /updateMeasurements.

- GET /measurements
  - Renders the measurements page (templates/measurements.html) and passes all measurements returned by MeasurementsDB.get_measurements().

- GET /updateMeasurements
  - Used by the front page script to fetch summary data (latest, min, max).
  - Response is JSON with the following fields (each returned as a SQL row tuple or null):
    - latCO2: [CO2_value, timestamp]
    - latTVOC: [TVOC_value, timestamp]
    - minCO2: [CO2_value, timestamp]
    - minTVOC: [TVOC_value, timestamp]
    - maxCO2: [CO2_value, timestamp]
    - maxTVOC: [TVOC_value, timestamp]

- POST /updateMeasurements
  - Used by the device to submit new measurements.
  - Required header: X-secret-key with the server-side secret. The key is currently hardcoded, and provides no security
  - POST JSON body fields (exact names expected by the server):
  - Responses:
    - 401 Unauthorized — if header X-secret-key does not match.
    - 400 Invalid JSON — missing or malformed JSON.
    - 422 Measurement is not a number — if the values cannot be cast to int.
    - 200 OK — on success; returns the same JSON payload as the GET (latest/min/max).

Database
--------
- File: Measurements.db (created by MeasurementsDB, default name "Measurements.db")
- Table (measurements) columns:
  - id INTEGER PRIMARY KEY AUTOINCREMENT
  - CO2 INTEGER NOT NULL
  - TVOC INTEGER NOT NULL
  - time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
- Queries implemented in db_handler.py:
  - add_measurement(CO2, TVOC)
  - get_measurements() — returns all rows ORDER BY time DESC
  - get_latest(mes_type) — latest CO2 or TVOC
  - get_min(mes_type) / get_max(mes_type)

