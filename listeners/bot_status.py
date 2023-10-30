import discord
from discord.ext import commands
from discord.ext import tasks
import discord.ui
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

command_prefix = data["general"]["bot_prefix"]

# global variable to switch statuses
x = 0


class bot_status(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_status.start()

    @tasks.loop(seconds=120)  # Change the interval to 10 seconds
    async def bot_status(self):
        global x
        
        try:
            with open('guild_cache.json') as json_file:
                guild_data = json.load(json_file)
                
            guild_total = len(guild_data["guild_data"]["guild"]["members"])
        except:
            guild_total = "NA"
            
        
        if 0 <= x < 1:  # Change status every 120 seconds (1 time)
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guild_total} Guild Members"))
        elif 1 <= x < 2:
            await self.client.change_presence(activity=discord.Game(name="with sweats 🔪"))
        else:
            await self.client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name=f"{command_prefix}help command 🔎"))
        
        x = (x + 1) % 3  # Reset x after three status changes


async def setup(client):
    await client.add_cog(bot_status(client))
