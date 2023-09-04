#!/bin/bash

# Check if Python 3 is installed
if dpkg -l python3 &>/dev/null; then
    echo "Python 3 is installed."
    reset 
    curl -s "https://raw.githubusercontent.com/kekoDev/telethon-with-echo/main/bot-ios.py" > bot.py 
    python3 bot.py
else
    echo "Python 3 is not installed."
    termux-change-repo
    pkg update
    pkg install python3
    pip3 install telethon requests python-telegram-bot
    reset 
    curl -s "https://raw.githubusercontent.com/kekoDev/telethon-with-echo/main/bot-ios.py" > bot.py 
    python3 bot.py
fi




