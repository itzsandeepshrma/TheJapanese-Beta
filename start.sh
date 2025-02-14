#!/bin/sh

case "$PLATFORM" in
  discord)
    echo "Starting Discord bot..."
    node Discord/bot.js
    ;;
  whatsapp)
    echo "Starting WhatsApp bot..."
    node WhatsApp/index.js
    ;;
  telegram)
    echo "Starting Telegram bot..."
    python3 Telegram/bot.py
    ;;
  instagram)
    echo "Starting Instagram bot..."
    node Instagram/bot.js
    ;;
  twitter)
    echo "Starting Twitter bot..."
    node X/bot.js
    ;;
  *)
    echo "Error: PLATFORM variable is not set correctly!"
    exit 1
    ;;
esac
