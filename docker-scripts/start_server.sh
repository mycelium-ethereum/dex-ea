#!/usr/bin/env bash

echo "$(date): Starting server" >> /var/log/cron.log 2>&1
cd /app
/usr/local/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8080