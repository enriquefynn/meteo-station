#!/usr/bin/env bash
curl -i \
    -H "Content-Type: application/json" \
    -X POST -d '{
        "date": "2023-09-17 12:00:00",
        "wind_direction": 15,
        "wind_speed_knot": 10,
        "precipitation_mm": 45,
        "temperature_c": 29,
        "pressure_mbar": 1020,
        "humidity": 30
        }' \
    http://127.0.0.1:5000/save_data