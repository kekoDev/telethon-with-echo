#!/bin/bash
apk get python3
apk get py-pip
pip install telethon
pip install python-telegram-bot
wget "https://raw.githubusercontent.com/kekoDev/telethon-with-echo/main/bot.py"
reset 
python3 bot.py
