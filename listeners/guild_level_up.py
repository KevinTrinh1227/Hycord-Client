import discord
from discord.ext import tasks, commands
import json
import discord
import discord.ui
import os
from dotenv import load_dotenv
import utils.guild_data as guild
import math

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
logs_channel_id = int(data["text_channel_ids"]["guild_news"])    # logs the bot logs in this channel
embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
guild_id = int(data["general"]["discord_server_guild_id"])

# Open the JSON file and read in the data
with open('guild_cache.json') as json_file:
    guild_data = json.load(json_file)["guild_data"]
total_guild_exp = guild_data["guild"]["exp"]
current_guild_level, _, _, _, _ = guild.get_guild_level_data(total_guild_exp)
current_guild_level = math.floor(current_guild_level)

class dailyguildlevelup(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.guild_id = guild_id
        self.dailyguildlevelup.start()

    @tasks.loop(seconds=10)  # Run every 60 seconds
    async def dailyguildlevelup(self):
        
        discord_guild = self.client.get_guild(guild_id)
        channel = self.client.get_channel(logs_channel_id)
        
        # Open the JSON file and read in the data
        with open('guild_cache.json') as json_file:
            guild_data = json.load(json_file)["guild_data"]["guild"]
            
        guild_name = guild_data['name']
        total_guild_exp = guild_data["exp"]
        guild_level, current_exp, exp_needed, exp_remaining, total_exp = guild.get_guild_level_data(total_guild_exp)
        
        new_guild_level = math.floor(guild_level)
        
        global current_guild_level
        
        if new_guild_level > current_guild_level:
            # print(f"{new_guild_level} > {current_guild_level}")
            # print(f"Guild Level Up! Level is: {new_guild_level}! Before Level: {current_guild_level}")
            
            embed = discord.Embed(
                title=(f"🎉 | {guild_name} Level Up! - [Lvl. {current_guild_level} ➜ Lvl. {new_guild_level}]"),
                description=f"The guild has just ranked up to level **{new_guild_level}**. Thank you to everyone who has contributed guild points! Total GEXP: `{'{:,}'.format(total_guild_exp)}`.",
                colour= embed_color
            )
            # embed.timestamp = datetime.datetime.now()
            embed.set_thumbnail(url = discord_guild.icon.url)
            # embed.set_footer(text=f"©️ {guild.name}", icon_url = guild.icon.url)
            
            await channel.send(embed=embed)
            current_guild_level = new_guild_level  # Update the current_guild_level
        else:
            #print(f"NO level up. Same lvl.")
            pass
        
        
async def setup(client):
    await client.add_cog(dailyguildlevelup(client))
