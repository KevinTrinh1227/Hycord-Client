"""
    Project name: Hycord Discord Bot
    Author: Kevin Huy Trinh
    Date created: Dec, 2022
    Native Version: 3.11.x
    Link: https://www.hycord.net
"""

from dotenv import load_dotenv
import client
import json
import os



load_dotenv()
discord_bot_application_id = os.getenv("DISCORD_APPLICATION_ID")
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

with open('config.json') as json_file:
    data = json.load(json_file)

# json data to run bot
bot_prefix = data["general"]["bot_prefix"]

if __name__ == "__main__":
   client.activateBot(discord_bot_token, bot_prefix, discord_bot_application_id)
