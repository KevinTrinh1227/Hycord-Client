import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import json
import pytz
import discord
import requests
import discord.ui
import os
from dotenv import load_dotenv
import time
from utils.guild_data import *
from utils.guild_data import *
from utils.pillow import *

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)


enable_feature = bool(data["features"]["auto_daily_gexp"])

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
hypixel_guild_id = data["hypixel_ids"]["guild_id"]
daily_points_channel_id = int(data["text_channel_ids"]["daily_guild_points"])
guild_id = int(data["general"]["discord_server_guild_id"])
command_prefix = data["general"]["bot_prefix"]


already_sent = False

class guild_discord_nick_updater(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.guild_id = guild_id
        self.guild_discord_nick_updater.start()
        
    @tasks.loop(seconds=10)  # Run every 60 seconds
    async def guild_discord_nick_updater(self):
        print("GUILD MEMBER NICKNAME UPDATER")
        
        
async def setup(client):
    await client.add_cog(guild_discord_nick_updater(client))