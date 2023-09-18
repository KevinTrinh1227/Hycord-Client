import discord
from discord.ext import commands
import aiohttp
import json
import datetime

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='meme')
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.com/gimme') as response:
                meme = await response.json()

        embed = discord.Embed(
            title=meme['title'],
            url=meme['postLink'],
            color=embed_color 
            )
        embed.set_image(url=meme['url'])
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"{ctx.guild.name}", icon_url = ctx.guild.icon.url)

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Meme(client))