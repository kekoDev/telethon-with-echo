#!/bin/bash
pkg update
pkg install openssl -y
pkg install python -y
pkg install python-pip -y
pip3 install telethon
pip3 install requests
pip3 install python-telegram-bot
wget "https://raw.githubusercontent.com/kekoDev/telethon-with-echo/main/bot.py"
reset 
python3 bot.py

