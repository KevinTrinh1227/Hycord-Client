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
import utils.guild_data as guild


with open('config.json') as json_file:
    data = json.load(json_file)
    
with open('guild_cache.json') as json_file:
    guild_data = json.load(json_file)["guild_data"]["guild"]

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
hypixel_guild_id = data["hypixel_ids"]["guild_id"]


class guildInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.hybrid_command(aliases = ["gi"], brief="guildinfo", description="Shows your general guild information", with_app_command=True)
    @commands.cooldown(1, 30, commands.BucketType.user) # 20 seconds.
    async def guildinfo(self, ctx):
        
        
        try:
            
            guild_name = guild_data['name']
            created_timestamp = guild_data['created']
            total_guild_exp = guild_data['exp']
            guild_description = guild_data['description']
            
            try:
                guild_master_uuid = guild_data["members"][0]["uuid"]
                g_master_url = f"https://api.mojang.com/user/profile/{guild_master_uuid}"
                g_response = requests.get(g_master_url)

                g_data = g_response.json()
                g_name = g_data["name"]
                guild_stats_link = f"https://plancke.io/hypixel/guild/player/{g_name}"
            except:
                g_name = "Not Available"
                guild_stats_link = f"https://plancke.io/hypixel/guild/"
            
            # for guilds who dont have tags yet
            try:
                guild_tag = guild_data['tag']
            except KeyError:
                guild_tag = "No Tag Available"
                
            guild_id = guild_data['_id']
            guild_level, current_exp, exp_needed, exp_remaining, total_exp = guild.get_guild_level_data(total_guild_exp)
            
            total_members = len(guild_data['members'])
            

            # Calculate the guild's age in months
            current_time = int(time.time() * 1000)  # Get the current time in milliseconds
            guild_age_ms = current_time - created_timestamp
            guild_age = guild_age_ms / (1000 * 60 * 60 * 24 * 30)  # Convert milliseconds to months

            
            embed = discord.Embed(
                title = f"**{guild_name} Guild Info**", 
                description=f"""
                Now displaying general guild stats for {guild_name}.
                
                - **Guild Master:** [{g_name}](https://plancke.io/hypixel/player/stats/{guild_master_uuid})
                - **Guild Tag:** [{guild_tag}]
                - **Guild ID:** `{guild_id}`
                - **Total Members:** `{total_members}`/`125`
                - **Total Guild EXP:** {total_guild_exp} EXP
                - **Guild Level:** {guild_level}
                - **GEXP to Next Level:** `{current_exp}`/`{exp_needed}`
                - **GEXP Remaining:** {exp_remaining}
                - **Guild Age:** {guild_age:.2f} month(s) old
                - **Description:** {guild_description}
                - **Stats Link:** [{guild_name} Plancke.io Link]({guild_stats_link})
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
    await client.add_cog(guildInfo(client))
    

