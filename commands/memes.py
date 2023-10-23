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

  @commands.hybrid_command(aliases=["memes", "dm", "dank"], brief="meme",description="Displays a random meme", with_app_command=True)
  async def meme(self, ctx: commands.Context):
    try: 
      async with aiohttp.ClientSession() as session:
        async with session.get('https://meme-api.com/gimme') as response:
          meme = await response.json()

      embed = discord.Embed(
        color=embed_color 
        )
      embed.set_image(url=meme['url'])

      await ctx.send(embed=embed)
       
    except:
      await ctx.send("Error generating meme.")

async def setup(client):
    await client.add_cog(Meme(client))