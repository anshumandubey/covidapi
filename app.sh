#!/usr/bin/env bash

export FLASK_APP=$(pwd)/api.py
chmod +x api.py
while true
do
    python3 -m flask run --host=0.0.0.0 &
    sleep 4h
    kill -9 $(pgrep -f flask)
    echo "Updating data.."
done