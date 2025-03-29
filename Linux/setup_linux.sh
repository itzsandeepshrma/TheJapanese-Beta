#!/bin/bash

LOGFILE="setup.log"

echo "Starting Full Setup for Team Japanese Userbot on Linux..." | tee -a $LOGFILE

echo "Installing dependencies (Python, Node.js, Git)..." | tee -a $LOGFILE
sudo apt update && sudo apt install -y python3 python3-pip nodejs npm git || { echo "Dependency installation failed!" | tee -a $LOGFILE; exit 1; }

if [ -d "TheJapanese" ]; then
    echo "Updating existing repository..." | tee -a $LOGFILE
    cd TheJapanese && git pull
else
    echo "Cloning the repository..." | tee -a $LOGFILE
    git clone https://github.com/TeamJapanese/TheJapanese.git TheJapanese || { echo "Clone failed!" | tee -a $LOGFILE; exit 1; }
    cd TheJapanese
fi

echo "Installing Python dependencies..." | tee -a $LOGFILE
pip3 install -r requirements.txt || { echo "Python dependencies installation failed!" | tee -a $LOGFILE; exit 1; }

if [ -f "package.json" ]; then
    echo "Installing JavaScript (Node.js) dependencies..." | tee -a $LOGFILE
    npm install || { echo "Node.js dependencies installation failed!" | tee -a $LOGFILE; exit 1; }
else
    echo "No package.json found, skipping Node.js dependencies installation." | tee -a $LOGFILE
fi

echo "Setting up auto-start on Linux (systemd)..." | tee -a $LOGFILE
SERVICE_FILE="/etc/systemd/system/teamjapanese.service"

sudo bash -c "cat <<EOL > $SERVICE_FILE
[Unit]
Description=Team Japanese Userbot
After=network.target

[Service]
Type=simple
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 userbot.py & /usr/bin/node bot.js
Restart=always
User=$(whoami)

[Install]
WantedBy=multi-user.target
EOL"

sudo systemctl daemon-reload
sudo systemctl enable teamjapanese
sudo systemctl start teamjapanese

echo "Starting the bot (Python + Node.js)..." | tee -a $LOGFILE
python3 userbot.py & 
node bot.js & 

echo "Setup complete! Bot is now running and will auto-start on boot." | tee -a $LOGFILE
