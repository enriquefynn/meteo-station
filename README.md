# Meteo-station
## Logs and serves data from a meteorological weather station:

## Installing requirements:
```
pip install -r server/requirements.txt
```

## Running:
```
./server/main.py
```

## API:

### PUT
- /save_data: Saves data in the json format:
```
{
    "date": <%Y-%m-%d %H:%M:%S>,
    "wind_direction": <int degrees>,
    "wind_speed_knot": <int speed in knots>,
    "precipitation_mm": <int precipitation in mm>,
    "temperature_c": <int temperature in degrees Celcius>,
    "pressure_mbar": <int temperature in millibars>,
    "humidity": <int humidity in %>
}
```

### GET
- /get_instant_data: Returns the latest data saved in the database. Returns data in the format:
```
{
    "date": <%Y-%m-%d %H:%M:%S>,
    "wind_direction": <int degrees>,
    "wind_speed_knot": <int speed in knots>,
    "precipitation_mm": <int precipitation in mm>,
    "temperature_c": <int temperature in degrees Celcius>,
    "pressure_mbar": <int temperature in millibars>,
    "humidity": <int humidity in %>
}
```
- /get_daily_data: Returns daily data grouped by hour from the current date. Returns data in the format:
```
[{
    "date": <%Y-%m-%d %H:%M:%S>,
    "avg_wind_direction": <int degrees>,
    "avg_wind_speed_knot": <int speed in knots>,
    "total_precipitation_mm": <int precipitation in mm>,
    "avg_temperature_c": <int temperature in degrees Celcius>,
    "avg_pressure_mbar": <int temperature in millibars>,
    "avg_humidity": <int humidity in %>
}]
```
- /get_weekly_data: Returns weekly data grouped by 6 hours from the current date. Returns data same as above.
- /get_monthly_data: Returns monthly data grouped by day from the current date. Returns data same as above.