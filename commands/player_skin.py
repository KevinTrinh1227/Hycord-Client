import discord
from discord.ext import commands
import requests
import discord.ui
import datetime
import json
import os
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests


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
            

            front_skin_url = f"https://starlightskins.lunareclipse.studio/skin-render/default/{uuid}/full"
            back_skin_url = f"https://visage.surgeplay.com/full/832/{uuid}.png?no=cape&y=140"

            background_image = Image.open("./assets/backgrounds/player_skin.png")

            front_response = requests.get(front_skin_url)
            front_skin = Image.open(BytesIO(front_response.content))

            back_response = requests.get(back_skin_url)
            back_skin = Image.open(BytesIO(back_response.content))

            max_width = 600  
            max_height = 800  
            # Resize the download img
            front_skin.thumbnail((max_width, max_height))

            # Paste the downloaded image onto the background
            background_image.paste(front_skin, (220, 250), front_skin)
            background_image.paste(back_skin, (850, 235), back_skin)

            # Save the resulting image
            background_image.save("./assets/example_outputs/player_skin.png")

            """
            embed = discord.Embed(
                title = f"🔗  |  {username}\'s download link",
                url = f"https://crafatar.com/skins/{uuid}",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            #embed.set_image(url=f"https://visage.surgeplay.com/full/832/{uuid}.png?no=ears,cape&y=-40")
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            """
            
            await ctx.send(file=discord.File("./assets/example_outputs/player_skin.png"))
        except Exception as e:
            error_message = str(e)
            embed = discord.Embed(
                title = f"Username does not exist",
                url = f"https://mcchecker.net/",
                description = f"Username: `{username}`\n\nThe username you have entered does not exist. Please check your spelling and try again. (You can use https://mcchecker.net/ to validate the username)",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(error_message)
        
async def setup(client):
    await client.add_cog(minecraft_skin(client))     