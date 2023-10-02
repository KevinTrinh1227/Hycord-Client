import discord
from discord.ext import commands
import requests
import discord.ui
import asyncio
import datetime
import os
from dotenv import load_dotenv
import json
from discord import app_commands


""" ==========================================
* CONFIG.JSON SECTION
*
* This block creates a config.json for
* an initial bot setup with the following
* default values.
========================================== """

if not os.path.exists('config.json'):
    default_config = {
        "config": {
            "bool": 0
        },
        "general": {
            "bot_prefix": "!",
            "embed_color": "#FF0000",
            "discord_server_guild_id": ""
        },
        "features": {
            "filtered_chat": 0,
            "auto_gexp": 0,
            "inactivity_cmd": 0,
            "punishments_cmd": 0
        },
        "category_ids": {
            "tickets_category": ""
        },
        "voice_channel_ids": {
            "member_count": "",
            "members_online": "",
            "guild_member_online": ""
        },
        "text_channel_ids": {
            "welcome": "",
            "rules": "",
            "inactivity_notice": "",
            "staff_chat": "",
            "tickets_transcripts": "",
            "leave_messages": "",
            "daily_guild_points": ""
        },
        "role_ids": {
            "guild_member": "",
            "verified_member": "",
            "unverified_member": "",
            "staff_member": "",
            "bots": ""
        },
        "hypixel_ids": {
            "guild_id": ""
        }
    }

    with open('config.json', 'w') as config_file:
        json.dump(default_config, config_file, indent=2)
        
        
        


def activateBot (discord_bot_token, bot_prefix, discord_application_id):
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix = bot_prefix, case_insensitive=True, intents=intents, application_id = discord_application_id)
    client.remove_command("help") #removes the default help command
            

    # If the bot is already configured meaning that inside the config.json
    # ["config"]["bool"] == 1, then we run as normal.


    """ ==========================================
    * BOT START UP SECTION
    *
    * This block starts up the bot. Here it 
    * checks if the config.json has already been
    * configured. If it hasnt, then it only loads
    * loads up the listeners.command_errors, and
    * commands.initial_setup cog.
    ========================================== """
    @client.event
    async def on_ready():
        
        # Open the JSON file and read in the data
        with open('config.json') as json_file:
            data = json.load(json_file)
        
        name = client.user.name.upper()
        discriminator = client.user.discriminator.upper()
        print(f"\nLOGGED IN AS: {name}#{discriminator}")
        
        if data["config"]["bool"] == 0:
            await client.load_extension("listeners.command_errors")
            await client.load_extension('commands.initial_setup')
            await client.tree.sync()
            print("YOUR BOT REQUIRES AN INITIAL SETUP. 🟡")
            print("----------------------------------------------------------")
            for x in range(0, 10):
                print("* USE: \"/setup\" or \"!setup\" IN YOUR SERVER TO BEGIN.")
            print("----------------------------------------------------------")
                
        else:
            print("----------------------------------------------------------")
            await load_cogs()
            print (f"* {os.path.basename(__file__):<30}{'Successful 🟢':<30}")

            # Sync the commands to Discord.
            await client.tree.sync()

            print("----------------------------------------------------------")
            #change_stats_channels.start()
            

    async def load_cogs():
        #load in all listeners
        print(f"{'LISTENER FILES':<30}  {'LOAD STATUS':<30}")
        for filename in os.listdir("./listeners"):
            if filename.endswith(".py"):
                await client.load_extension(f"listeners.{filename[:-3]}")
                print (f"* {filename:<30}{'Successful 🟢':<30}")
        print(f"\n{'COMMAND FILES':<30}  {'LOAD STATUS':<30}")
        #load in all commands
        for filename in os.listdir("./commands"):
            if filename.endswith(".py"):
                await client.load_extension(f"commands.{filename[:-3]}")
                print (f"* {filename:<30}{'Successful 🟢':<30}")
        print(f"\n{'OTHER FILES':<30}  {'LOAD STATUS':<30}")
            
 
    
    client.run(discord_bot_token)
        