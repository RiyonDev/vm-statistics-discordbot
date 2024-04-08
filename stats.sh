#!/bin/bash

# Function to install dependencies
install_dependencies() {
    echo "Installing dependencies..."
    sudo apt update
    sudo apt install -y python3 python3-pip git
    pip3 install discord.py psutil
}

# Function to clone repository
clone_repository() {
    echo "Cloning repository..."
    git clone https://github.com/RiyonDev/vm-statistics-discordbot
}

# Function to collect bot information and insert into Python script
setup_bot() {
    echo "Please enter your bot token:"
    read -r TOKEN
    echo "Please enter your channel ID:"
    read -r CHANNEL_ID
    echo "Please enter the image URL for the embed thumbnail (leave empty if none):"
    read -r IMAGE_URL

    # Insert bot information into Python script
    sed -i "s|TOKEN = ''|TOKEN = '$TOKEN'|" vm-statistics-discordbot/bot.py
    sed -i "s|CHANNEL_ID =  1231312321|CHANNEL_ID = $CHANNEL_ID|" vm-statistics-discordbot/bot.py
    sed -i "s|IMAGE_URL = \"\"|IMAGE_URL = \"$IMAGE_URL\"|" vm-statistics-discordbot/bot.py
}

# Function to run the bot
run_bot() {
    echo "Starting the bot..."
    cd vm-statistics-discordbot
    python3 bot.py
}

# Main function
main() {
    install_dependencies
    clone_repository
    setup_bot
    run_bot
}

# Call the main function
main
