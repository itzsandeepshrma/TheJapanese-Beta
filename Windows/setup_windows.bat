@echo off
setlocal
set LOGFILE=setup.log

echo Starting Full Setup for Team Japanese Userbot on Windows... > %LOGFILE%

where choco >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Chocolatey... >> %LOGFILE%
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    setx PATH "%PATH%;%ProgramData%\chocolatey\bin"
) else (
    echo Chocolatey already installed! >> %LOGFILE%
)

echo Installing dependencies (Python, Node.js, Git)... >> %LOGFILE%
choco install python nodejs git -y || echo Dependency installation failed! >> %LOGFILE% && exit /b 1

if exist "TheJapanese" (
    echo Updating existing repository... >> %LOGFILE%
    cd TheJapanese && git pull
) else (
    echo Cloning the repository... >> %LOGFILE%
    git clone https://github.com/TeamJapanese/TheJapanese.git TheJapanese || echo Clone failed! >> %LOGFILE% && exit /b 1
    cd TheJapanese
)

echo Installing Python dependencies... >> %LOGFILE%
pip install -r requirements.txt || echo Python dependencies installation failed! >> %LOGFILE% && exit /b 1

if exist "package.json" (
    echo Installing JavaScript (Node.js) dependencies... >> %LOGFILE%
    npm install || echo Node.js dependencies installation failed! >> %LOGFILE% && exit /b 1
) else (
    echo No package.json found, skipping Node.js dependencies installation. >> %LOGFILE%
)

echo Setting up auto-start using Windows Task Scheduler... >> %LOGFILE%
schtasks /create /tn "TeamJapaneseUserbot" /tr "cmd /c cd %CD% && start python userbot.py & start node bot.js" /sc onlogon /rl highest

echo Starting the bot (Python + Node.js)... >> %LOGFILE%
start python userbot.py
start node bot.js

echo Setup complete! Bot is now running and will auto-start on boot. >> %LOGFILE%
