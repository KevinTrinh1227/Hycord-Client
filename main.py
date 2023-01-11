"""
    Project name: Streamer Discord Bot
    Author: Kevin Huy Trinh
    Date created: Dec, 2022
    Python Version: 3.11.1
    Description: Discord bot made towards streamer to aid them in 
        managing a discord community. This bot was made with the 
        intentions of only having 1 bot with all the functionalities. 
        
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
bot_prefix = data["bot_prefix"]
embed_color = data["embed_color"]
embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format


if __name__ == "__main__":
   client.activateBot(discord_bot_token, bot_prefix, embed_color)
