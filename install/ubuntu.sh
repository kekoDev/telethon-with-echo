#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    sudo apt install python3
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed."
    sudo apt install python3-pip

    pip3 install python-telegram-bot telethon

fi

# Install Python packages

# Check if the installation was successful
if [ $? -ne 0 ]; then
    echo "Failed to install Python packages."
    exit 1
fi

# Create a temporary file to store the downloaded script

# Download the Python script using wget
rm ios.py

curl "https://raw.githubusercontent.com/kekoDev/telethon-with-echo/main/bot-ios.py" > "ios.py"

# Run the downloaded Python script
python3 ios.py
