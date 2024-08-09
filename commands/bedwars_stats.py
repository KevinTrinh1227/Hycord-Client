import discord
from discord.ext import commands
import requests
import discord.ui
import datetime
import json
import os
from dotenv import load_dotenv
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests
import utils.pillow as pillow
from utils.player_functions import *
from utils.pillow import *


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
font_title = ImageFont.truetype("./assets/fonts/main.ttf", 17)
font_stat = ImageFont.truetype("./assets/fonts/main.ttf", 16)

minecraft_colors = {
    '0': (0, 0, 0),
    '1': (0, 0, 170),
    '2': (0, 170, 0),
    '3': (0, 170, 170),
    '4': (170, 0, 0),
    '5': (170, 0, 170),
    '6': (255, 170, 0),
    '7': (170, 170, 170),
    '8': (85, 85, 85),
    '9': (85, 85, 255),
    'a': (85, 255, 85),
    'b': (85, 255, 255),
    'c': (255, 85, 85),
    'd': (255, 85, 255),
    'e': (255, 255, 85),
    'f': (255, 255, 255),
    'r': (255, 85, 85),  # default rank color
    'p': (255, 170, 0)   # default plus color
}
    
class bedwarsstats(commands.Cog):
    def __init__(self, client):
        self.client = client
        
   
    #bedwars stats command
    @commands.hybrid_command(aliases=["bedwarstats", "bwstat", "bws"], brief="bws [Minecraft User Name]", description="View a players Bedwars Stats", with_app_command=True)
    async def bedwars(self, ctx: commands.Context, *, username: str):
        
        try:#if player exist it will work
            
            
            #load in .env variables
            load_dotenv() 

            #get hypixel api key
            hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
            
            url = f"https://api.mojang.com/users/profiles/minecraft/{username}?"
            response = requests.get(url)
            uuid = response.json()['id']

            requestlink = f"https://api.hypixel.net/v2/player?key={hypixel_api_key}&uuid={uuid}"
            hydata = requests.get(requestlink).json()
            #print(hydata)
            
            #finals stats
            bedwars_final_kills = hydata["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
            bedwars_final_deaths = hydata['player']['stats']['Bedwars']["final_deaths_bedwars"]
            bedwars_fkdr = round((bedwars_final_kills/bedwars_final_deaths), 2)
            
            #finals stats
            bedwars_kills = hydata["player"]["stats"]["Bedwars"]["kills_bedwars"]
            bedwars_deaths = hydata['player']['stats']['Bedwars']["deaths_bedwars"]
            bedwars_kdr = round((bedwars_kills/bedwars_deaths), 2)
            
            #beds broken stats
            bedwars_beds_broken = hydata['player']['stats']["Bedwars"]["beds_broken_bedwars"]
            bedwars_beds_lost = hydata['player']['stats']["Bedwars"]["beds_lost_bedwars"]
            bedwars_bed_bblr = round((bedwars_beds_broken/bedwars_beds_lost), 2)
            
            #wins and losses
            bedwars_wins = hydata['player']['stats']['Bedwars']["wins_bedwars"]
            bedwars_losses = hydata['player']['stats']['Bedwars']["losses_bedwars"]
            bedwars_wlr = round((bedwars_wins/bedwars_losses), 2)
            
            #other statistics
            bedwars_level = hydata["player"]["achievements"]["bedwars_level"] #bedwars level
            
            background_image = Image.open("./assets/backgrounds/bedwars_stats.png")
            
            try:
                headers = {
                    "User-Agent": "HycordBot/2.0 (+https://github.com/KevinTrinh1227/Hycord-Client; https://kevintrinh.dev)"
                }
                front_response = requests.get(f"https://visage.surgeplay.com/full/300/{uuid}.png?y=-50", headers=headers)
                front_skin = Image.open(BytesIO(front_response.content))
            except:
                front_skin = Image.open("./assets/resources/default_skin_front.png")
                
                
            # Paste the downloaded image onto the background
            background_image.paste(front_skin, (437, 38), front_skin)
            
            draw = ImageDraw.Draw(background_image)
            
            header_text = f"'s Stats"
            footer_text = f"© {ctx.guild.name}"
            
            # Draw the player tag and name with the correct colors
            player_name = username
            player_tags = get_player_tag(hydata)
            x, y = 222, 23  # Center position
            
            
            # Calculate the total width of player tags
            player_tags_width = sum(get_text_width(draw, component[1], font_title) for component in player_tags)
            # Calculate the widths of the player name and header text
            player_name_width = get_text_width(draw, player_name, font_title)
            header_text_width = get_text_width(draw, header_text, font_title)
            
            # Calculate the total width of all components including the spaces between them
            space_between_texts = 2
            total_width = player_tags_width + len(player_tags) * space_between_texts + player_name_width + space_between_texts + header_text_width
            
            # Calculate the starting x position to center the combined width at (x, y)
            start_x = x - (total_width / 2)
            
            # Draw each component at the calculated positions
            current_x = start_x
            for component in player_tags:
                color = minecraft_colors.get(component[0], (255, 255, 255))
                draw.text((current_x, y), component[1], fill=color, font=font_title)
                current_x += get_text_width(draw, component[1], font_title) + space_between_texts
            
            # Draw the player name
            name_color = minecraft_colors.get(player_tags[-1][0], (255, 255, 255)) if player_tags else (255, 255, 255)
            draw.text((current_x, y), player_name, fill=name_color, font=font_title)
            current_x += player_name_width + space_between_texts
            
            # Draw the header text
            draw.text((current_x, y), header_text, fill=(255, 255, 255), font=font_title)
            draw.text((pillow.center(222, footer_text, font_title),312), footer_text, (255, 255, 255), font=font_title)
            
            
            
            
            try:
                level_tag = get_bedwars_level_tag(bedwars_level)
                next_tag = get_bedwars_level_tag(((bedwars_level + 99) // 100) * 100)
                x,y = 530, 18
                # Calculate total width of the combined text
                total_width = sum(get_text_width(draw, component[1], font_stat) for component in level_tag)
                total_width += get_text_width(draw, " / ", font_stat)
                total_width += sum(get_text_width(draw, component[1], font_stat) for component in next_tag)

                # Adjust x to center the text at (525, 18)
                x_centered = x - total_width // 2

                # Draw the level tag
                for component in level_tag:
                    color_code = component[0]
                    text = component[1]
                    color = minecraft_colors.get(color_code, (255, 255, 255))  # Default to white if color code not found
                    draw.text((x_centered, y), text, fill=color, font=font_stat)
                    x_centered += get_text_width(draw, text, font_stat)

                # Draw the separator
                separator_text = " / "
                draw.text((x_centered, y), separator_text, fill=minecraft_colors['7'], font=font_stat)
                x_centered += get_text_width(draw, separator_text, font_stat)

                # Draw the next level tag
                for component in next_tag:
                    color_code = component[0]
                    text = component[1]
                    color = minecraft_colors.get(color_code, (255, 255, 255))  # Default to white if color code not found
                    draw.text((x_centered, y), text, fill=color, font=font_stat)
                    x_centered += get_text_width(draw, text, font_stat)
            except Exception as e:
                print(e)
            #draw.text((pillow.center(525, f"Lvl. {bedwars_level}", font_stat),18), f"Lvl. {bedwars_level}", (255, 255, 255), font=font_stat)
        
        
        
        
        
            # wins row
            draw.text((pillow.center(70, bedwars_wins, font_stat), 90), f"{bedwars_wins}", (255, 255, 255), font=font_stat)
            draw.text((pillow.center(222, bedwars_losses, font_stat), 90), f"{bedwars_losses}", (255, 255, 255), font=font_stat)
            draw.text((pillow.center(360, bedwars_wlr, font_stat), 90), f"{bedwars_wlr}", (255, 255, 255), font=font_stat)

            # finals row
            draw.text((pillow.center(70, bedwars_final_kills, font_stat), 147), f"{bedwars_final_kills}", (255, 255, 255), font=font_stat)
            draw.text((pillow.center(222, bedwars_final_deaths, font_stat), 147), f"{bedwars_final_deaths}", (255, 255, 255), font=font_stat)
            draw.text((pillow.center(360, bedwars_fkdr, font_stat), 147), f"{bedwars_fkdr}", (255, 255, 255), font=font_stat)

            # beds stats row50
            draw.text((pillow.center(70, bedwars_beds_broken, font_stat), 208), f"{bedwars_beds_broken}", (255, 255, 255), font=font_stat)
            draw.text((pillow.center(222, bedwars_beds_lost, font_stat), 208), f"{bedwars_beds_lost}", (255, 255, 255), font=font_stat)
            draw.text((pillow.center(360, bedwars_bed_bblr, font_stat), 208), f"{bedwars_bed_bblr}", (255, 255, 255), font=font_stat)

            # normal kills
            draw.text((pillow.center(70, bedwars_kills, font_stat), 267), f"{bedwars_kills}", (255, 255, 255), font=font_stat)
            draw.text((pillow.center(222, bedwars_deaths, font_stat), 267), f"{bedwars_deaths}", (255, 255, 255), font=font_stat)
            draw.text((pillow.center(360, bedwars_kdr, font_stat), 267), f"{bedwars_kdr}", (255, 255, 255), font=font_stat)
   
            background_image.save("./assets/outputs/bedwars_stats.png") # save the img
            
            await ctx.send(file=discord.File("./assets/outputs/bedwars_stats.png"))
            
            """
            #player embed
            embed = discord.Embed(
                title = f"**[{bedwars_level}✫] {username}'s Bedwars Stats**",
                # url = f"https://plancke.io/hypixel/player/stats/{username}",
                description = f"`{uuid}`",
                color = embed_color
            )
            # embed.set_author(name = f"{username}'s Profile", icon_url = f"https://crafatar.com/avatars/{uuid}")
            embed.timestamp = datetime.datetime.now()
            embed.add_field(name='Final Kills', value=bedwars_final_kills, inline=True)
            embed.add_field(name='Final Deaths', value=bedwars_final_deaths, inline=True)
            embed.add_field(name='FKDR', value=bedwars_fkdr, inline=True)
            embed.add_field(name='Wins', value=bedwars_wins, inline=True)
            embed.add_field(name='Losses', value=bedwars_losses, inline=True)
            embed.add_field(name='WLR', value=bedwars_wlr, inline=True)
            embed.add_field(name='Beds Broken', value=bedwars_wins, inline=True)
            embed.add_field(name='Beds Lost', value=bedwars_beds_lost, inline=True)
            embed.add_field(name='BBLR', value=bedwars_bed_bblr, inline=True)
            embed.add_field(name='Kills', value=bedwars_kills, inline=True)
            embed.add_field(name='Deaths', value=bedwars_deaths, inline=True)
            embed.add_field(name='KDR', value=bedwars_kdr, inline=True)
            embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/{uuid}.png?y=-40")
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed)
            """
        except:     #if player does not exist
            embed = discord.Embed(
                title="User Does Not Exist",
                url="https://mcchecker.net/",
                description=f"Username: `{username}`\n\nThe username you have entered does not exist or an error occurred. Please check your spelling and try again. (You can use https://mcchecker.net/ to validate the username)",
                color=discord.Color.red()
            )
            embed.timestamp = datetime.datetime.now()
            if ctx.author.avatar:  # Check if the author has an avatar
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            else:
                embed.set_footer(text=f"Requested by {ctx.author}")
            
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(bedwarsstats(client))