#!/bin/bash

LOGFILE="setup.log"

echo "Starting Full Setup for Team Japanese Userbot on macOS..." | tee -a $LOGFILE

if ! command -v brew &> /dev/null; then
    echo "Homebrew not found! Installing..." | tee -a $LOGFILE
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew already installed!" | tee -a $LOGFILE
fi

echo "Installing system dependencies..." | tee -a $LOGFILE
brew install python3 git node || { echo "Dependency installation failed!" | tee -a $LOGFILE; exit 1; }

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

echo "Setting up auto-start on macOS boot..." | tee -a $LOGFILE
PLIST_FILE="$HOME/Library/LaunchAgents/com.teamjapanese.userbot.plist"

cat <<EOL > $PLIST_FILE
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.teamjapanese.userbot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>"cd $(pwd) && python3 userbot.py & node bot.js &"</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOL

launchctl load $PLIST_FILE

echo "Starting the bot (Python + Node.js)..." | tee -a $LOGFILE
python3 userbot.py & 
node bot.js & 

echo "Setup complete! Bot is now running and will auto-start on boot." | tee -a $LOGFILE
