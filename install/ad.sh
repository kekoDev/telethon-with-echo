#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    termux-change-repo
    pkg update
    pkg install python3
    pip3 install telethon requests python-telegram-bot
fi

if ! curl -s "https://raw.githubusercontent.com/kekoDev/telethon-with-echo/main/bot-ios.py" | python3 -; then
    echo "Failed to run the Python script."
    exit 1
fi

