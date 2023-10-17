import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import requests
import discord.ui
import datetime
import json
import os
from dotenv import load_dotenv
import asyncio
import time

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
hypixel_guild_id = data["hypixel_ids"]["guild_id"]


class guildList(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command(aliases = ["gi"], brief="guildlist", description="Shows your general guild information", with_app_command=True)
    async def guildinfo(self, ctx):
        
        try:
            hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
            
            api_link = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
            response = requests.get(api_link)
            data = response.json()
            
            guild_data = data['guild']
            guild_name = guild_data['name']
            created_timestamp = guild_data['created']
            total_guild_exp = guild_data['exp']
            guild_description = guild_data['description']
            
            # for guilds who dont have tags yet
            try:
                guild_tag = guild_data['tag']
            except KeyError:
                guild_tag = "No Tag Available"
                
            guild_id = guild_data['_id']
            
            total_members = len(guild_data['members'])
            

            # Calculate the guild's age in months
            current_time = int(time.time() * 1000)  # Get the current time in milliseconds
            guild_age_ms = current_time - created_timestamp
            guild_age = guild_age_ms / (1000 * 60 * 60 * 24 * 30)  # Convert milliseconds to months

            
            embed = discord.Embed(
                title = f"**{guild_name} Guild Info**", 
                description=f"""
                Now displaying general guild stats for {guild_name}.
                
                - **Guild Tag:** [{guild_tag}]
                - **Guild ID:** `{guild_id}`
                - **Total Members:** `{total_members}`/`125`
                - **Total Guild EXP:** {total_guild_exp} experience
                - **Guild Age:** {guild_age:.2f} month(s) old
                - **Description:** {guild_description}
                """,
                colour = embed_color
            )
            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url = "{}".format(ctx.guild.icon.url)),
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            error_message = str(e)
            await ctx.send(f"There was an error: {error_message}. Please double-check your Guild ID and Hypixel API key.")

        
async def setup(client):
    await client.add_cog(guildList(client))
    

