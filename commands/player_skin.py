import discord
from discord.ext import commands
import requests
import discord.ui
import datetime
import json
import os
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    

class minecraft_skin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}
            
    #bedwars stats command
    @commands.hybrid_command(aliases=["playerskin"], brief="skin [Minecraft IGN]", description="Displays the skin of the specified player", with_app_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user) # 1 use for every 10 seconds.
    async def skin(self, ctx, *, username):
        
        try:
            url = f"https://api.mojang.com/users/profiles/minecraft/{username}?"
            response = requests.get(url)
            uuid = response.json()['id']

            embed = discord.Embed(
                title = f"🔗  |  {username}\'s download link",
                url = f"https://crafatar.com/skins/{uuid}",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_image(url=f"https://visage.surgeplay.com/full/832/{uuid}.png?no=ears,cape&y=-40")
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title = f"Username does not exist",
                url = f"https://mcchecker.net/",
                description = f"Username: `{username}`\n\nThe username you have entered does not exist. Please check your spelling and try again. (You can use https://mcchecker.net/ to validate the username)",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(minecraft_skin(client))     