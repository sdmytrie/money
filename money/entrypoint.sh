#!/usr/bin/env bash
cd /app
python3 -m daphne money.asgi:application -b money
