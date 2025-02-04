#!/bin/bash

while true; do
    echo "🚀 Starting The-Japanese..."
    python3 -m Telegram
    echo "⚠️ Bot crashed! Restarting in 5 seconds..."
    sleep 5
done


# 🔹 For VPS: Run chmod +x start.sh and start with ./start.sh.
# 🔹 For Local: Simply run python3 -m Telegram.

