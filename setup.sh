#!/bin/bash
echo "🔹 Installing Python Dependencies..."
pip install -r requirements.txt

echo "🔹 Installing Node.js Dependencies..."
cd TheJapanese/Instagram && npm install
cd ../WhatsApp && npm install

echo "✅ Setup Complete!"
