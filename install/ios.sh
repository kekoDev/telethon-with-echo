#!/bin/bash
apk add python3
apk add py-pip
pip install python-telegram-bot telethon
wget "https://raw.githubusercontent.com/kekoDev/telethon-with-echo/main/bot.py"
reset 
python3 bot.py 

