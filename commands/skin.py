import discord
from discord.ext import commands
import requests
import discord.ui
import datetime
import json
import os
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests
from discord.ui import Button, View


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    

embed_color = int(data["general"]["embed_color"].strip("#"), 16) 
font_title = ImageFont.truetype("./assets/fonts/main.ttf", 60)
font_footer = ImageFont.truetype("./assets/fonts/main.ttf", 40)
    

class minecraft_skin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}
            
    # playerskin
    @commands.hybrid_command(aliases=["playerskin"], brief="skin [Minecraft IGN]", description="Displays the skin of the specified player", with_app_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user) # 1 use for every 10 seconds.
    async def skin(self, ctx, *, username):
        
        try:            
            url = f"https://api.mojang.com/users/profiles/minecraft/{username}?"
            response = requests.get(url)
            uuid = response.json()['id']
            
            background_image = Image.open("./assets/backgrounds/transparent_1000_1000.png")
            try:
                headers = {
                    "User-Agent": "HycordBot/2.0 (+https://github.com/KevinTrinh1227/Hycord-Client; https://kevintrinh.dev)"
                }
                front_skin_url = f"https://visage.surgeplay.com/full/832/{uuid}.png?no=cape"
                back_skin_url = f"https://visage.surgeplay.com/full/832/{uuid}.png?no=cape&y=140"

                front_response = requests.get(front_skin_url, headers=headers)
                front_skin = Image.open(BytesIO(front_response.content))

                back_response = requests.get(back_skin_url, headers=headers)
                back_skin = Image.open(BytesIO(back_response.content))
            except:
                front_skin = Image.open("./assets/resources/default_skin_front.png")
                back_skin = Image.open("./assets/resources/default_skin_back.png")
                

            # front_skin.thumbnail((600, 800)) # resize
            
            # Calculate the center x-coordinate for text
            image_width, _ = background_image.size
            text1 = f"{username}'s Skin"
            text2 = f"\u00a9\ufe0f {ctx.guild.name}"

            draw = ImageDraw.Draw(background_image)

            _, _, text1_width, _ = draw.textbbox((0, 0), text1, font=font_title)
            _, _, text2_width, _ = draw.textbbox((0, 0), text2, font=font_footer)

            center_x1 = (image_width - text1_width) // 2
            center_x2 = (image_width - text2_width) // 2

            # Paste the downloaded image onto the background
            background_image.paste(front_skin, (10, 150), front_skin)
            background_image.paste(back_skin, (510, 150), back_skin)
            
            draw = ImageDraw.Draw(background_image)
            draw.text((center_x1,50), text1, (255, 255, 255), font=font_title)
            draw.text((center_x2,1050), text2, (255, 255, 255), font=font_footer)

            background_image.save("./assets/outputs/player_skin.png") # save the img

            #await ctx.send(file=discord.File("./assets/outputs/player_skin.png"))
            
            # Create buttons
            button1 = Button(label="Download Skin", url=f"https://crafatar.com/skins/{uuid}")
            button2 = Button(label="NameMC", url=f"https://namemc.com/profile/{uuid}")
            button3 = Button(label="View", url=f"https://vzge.me/full/832/{uuid}.png")

            # Create a View and add buttons to it
            view = View()
            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)

            # Send the image file along with the buttons in a single message
            await ctx.send(
                file=discord.File("./assets/outputs/player_skin.png"),
                view=view
            )
            
        except Exception as e:
            error_message = str(e)
            print(error_message)
            embed = discord.Embed(
                title = f"Username does not exist",
                url = f"https://mcchecker.net/",
                description = f"Username: `{username}`\n\nThe username you have entered does not exist. Please check your spelling and try again. (You can use https://mcchecker.net/ to validate the username)",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            if(ctx.author.avatar):
                embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            else:
                embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.guild.icon.url)
            
            await ctx.send(embed=embed)
            
            
            
    # player skin download feature
    @commands.hybrid_command(aliases=["downloadskin"], brief="skindownload [Minecraft IGN]", description="Gets a specific player's skin download link", with_app_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user) # 1 use for every 10 seconds.
    async def skindownload(self, ctx, *, username):
        
        try:            
            url = f"https://api.mojang.com/users/profiles/minecraft/{username}?"
            response = requests.get(url)
            uuid = response.json()['id']

            # await ctx.send(f"https://crafatar.com/skins/{uuid}")
            
            
            embed = discord.Embed(
                description=f"[Download Link](https://crafatar.com/skins/{uuid})",
                color = embed_color
            )
            embed.set_image(url=f"https://crafatar.com/skins/{uuid}")
            await ctx.send(embed=embed)
            
        except Exception as e:
            error_message = str(e)
            print(error_message)
            embed = discord.Embed(
                title = f"Username does not exist",
                url = f"https://mcchecker.net/",
                description = f"Username: `{username}`\n\nThe username you have entered does not exist. Please check your spelling and try again. (You can use https://mcchecker.net/ to validate the username)",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            if(ctx.author.avatar):
                embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            else:
                embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.guild.icon.url)
            
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(minecraft_skin(client))     