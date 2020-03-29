#!/usr/bin/env bash

export FLASK_APP=$(pwd)/api.py
chmod +x api.py
while true
do
    python3 -m flask run &
    sleep 4h
    kill -9 $(pgrep -f flask)
    echo "Updating data.."
done