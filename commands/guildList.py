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


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
hypixel_guild_id = data["hypixel_ids"]["guild_id"]


class guildList(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #chat purge command (and command removal)   
    @commands.has_permissions(manage_messages = True)
    @commands.command(aliases = ["gl"], brief="guildlist",description="Show a list of all guild members")
    async def guildlist(self, ctx):
        
        hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
        
        #adding the typing effect
        async with ctx.typing():
            await asyncio.sleep(1)

        api_link = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
        response = requests.get(api_link)
        data = response.json()
        
        guild_name = data['guild']['name']

        players = []
        for i, member in enumerate(data['guild']['members']):
            uuid = member['uuid']
            username_api = f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}'
            response = requests.get(username_api)
            data = response.json()
            username = data['name']
            rank = member['rank']
            players.append(f'***{i+1}.*** {username} - {rank} - `{uuid}`')
            total_members = len(players)

        # Send the usernames as a message to the Discord server
        embed_string = "\n".join(players)
        
        embed = discord.Embed(
            title = f"**{guild_name} Guild List**", 
            description=f"**Total Members:** `{total_members}`/`125`\n\nNow displaying each guild member's username, rank, and uuid.\n\n{embed_string}",
            colour = embed_color
        )
        embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url = "{}".format(ctx.guild.icon.url)),
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
        await ctx.send(embed=embed)

        
async def setup(client):
    await client.add_cog(guildList(client))
    

