"""
    Project name: Hycord Discord Bot
    Author: Kevin Huy Trinh
    Date created: Dec, 2022
    Python Version: 3.11.1
    Description: Hycord is an all-in-one Discord Python program for Hypixel players, 
        providing easy access to comprehensive data and statistics. With an extensive library
        of commands, Hycord allows users to link and validate accounts, moderate community 
        servers, and retrieve accurate player data, making it a powerful tool for streamlining 
        server functionality. Become part of the Hycord community today and enjoy top-notch 
        performance and accuracy with just one bot.
"""

from dotenv import load_dotenv
import client
import json
import os

#load in .env variables

load_dotenv() 

discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

#json data to run bot
bot_prefix = data["general"]["bot_prefix"]
embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format


if __name__ == "__main__":
   client.activateBot(discord_bot_token, bot_prefix, embed_color)
