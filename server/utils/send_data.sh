#!/usr/bin/env bash
curl -i \
    -H "Content-Type: application/json" \
    -X POST -d "{
        \"date\": \"$2\",
        \"wind_direction\": 2,
        \"wind_speed_knot\": 15,
        \"temperature_c\": 23,
        \"pressure_mbar\": 0,
        \"humidity\": 30
        }" \
    http://$1:5080/save_air_data
