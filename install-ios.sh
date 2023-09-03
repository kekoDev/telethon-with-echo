#!/bin/bash
apk get python3
apk get py-pip
pip install telethon
pip install python-telegram-bot
reset 
python3 bot.py
