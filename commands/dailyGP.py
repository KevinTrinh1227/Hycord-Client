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


class dailygp(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #chat purge command (and command removal)   
    @commands.has_permissions(manage_messages = True)
    @commands.command(aliases = ["dgp", "dailypoints", "dp"], brief="dailypoints",description="Show the guild's daily points earned")
    async def dailygp(self, ctx):
        
        hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
        
        #adding the typing effect
        async with ctx.typing():
            await asyncio.sleep(1)

        api_link = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
        response = requests.get(api_link)
        data = response.json()
        
        guild_name = data['guild']['name']

        members = data['guild']['members']
        sorted_members = sorted(members, key=lambda x: sum(x['expHistory'].values()), reverse=True)

        players = []
        for i, member in enumerate(sorted_members): # loop through first 10 sorted members only
            uuid = member['uuid']
            username_api = f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}'
            response = requests.get(username_api)
            data = response.json()
            username = data['name']
            exp_history = member['expHistory']
            if exp_history:
                today = datetime.date.today().strftime("%Y-%m-%d") # Hypixel GMT is 8 hours ahead of Pacific time
                if today in exp_history:
                    exp_today = int(exp_history[today])
                    new_member = (username, exp_today)
                    players.append(new_member)
                else:
                    pass
            else:
                pass
        
        output = []
        new_users_sorted = sorted(players, key=lambda x: x[1], reverse=True)

        total_exp = 0
        for i, (user, exp_today) in enumerate(new_users_sorted):
            output.append(f"{i+1}.  {user}  -  {exp_today} GEXP")
            total_exp += exp_today

        embed_string = "\n".join(output)
        
        embed = discord.Embed(
            title = f"**{guild_name} Guild Points**", 
            description=f"A total of `{total_exp}` was earned thus far as of {today}\n\n```{embed_string}```",
            colour = embed_color
        )
        embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url = "{}".format(ctx.guild.icon.url)),
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
        await ctx.send(embed=embed)

        
async def setup(client):
    await client.add_cog(dailygp(client))
    

