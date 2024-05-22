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
    
    
# Check if the file exists
file_name = 'verified_accounts.json'
if os.path.exists(file_name):
    # print(f"The file '{file_name}' already exists.")
    pass
else:
    # Create the file
    with open(file_name, 'w') as file:
        file.write('{}')  # Writing an empty JSON object
    print(f"The file '{file_name}' has been created.")

# json data to run bot
bot_prefix = data["general"]["bot_prefix"]

if __name__ == "__main__":
   client.activateBot(discord_bot_token, bot_prefix, discord_bot_application_id)
