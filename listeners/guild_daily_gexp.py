import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import json
import pytz
import discord
import requests
import discord.ui
import os
from dotenv import load_dotenv
import time
from utils.guild_data import *
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from utils.guild_data import *
from utils.pillow import *

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)


enable_feature = bool(data["features"]["auto_daily_gexp"])

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
hypixel_guild_id = data["hypixel_ids"]["guild_id"]
daily_points_channel_id = int(data["text_channel_ids"]["daily_guild_points"])
guild_id = int(data["general"]["discord_server_guild_id"])
command_prefix = data["general"]["bot_prefix"]

font_title = ImageFont.truetype("./assets/fonts/Minecraft.ttf", 22)
font_footer = ImageFont.truetype("./assets/fonts/Minecraft.ttf", 14)
font_username = ImageFont.truetype("./assets/fonts/Minecraft.ttf", 14)

already_sent = False

class dailygpoints(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.guild_id = guild_id
        self.dailygpoints.start()
        self.total_points = 0  # Initialize the total points variable

    @tasks.loop(seconds=60)  # Run every 60 seconds
    async def dailygpoints(self):
        global already_sent
        if enable_feature:
            channel = self.client.get_channel(daily_points_channel_id)
            guild = self.client.get_guild(self.guild_id)
            est = pytz.timezone('US/Eastern')
            current_time = datetime.now(est)
            
            if current_time.hour == 0 and current_time.minute == 0: # 00:00 mid night EST
                if not already_sent:
                    
                    # Load the "verified_accounts.json" file as a dictionary
                    with open('verified_accounts.json', 'r') as verified_file:
                        verified_accounts = json.load(verified_file)
                        
                    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                    hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
                    api_link = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
                    response = requests.get(api_link)

                    if response.status_code == 200:
                        data = response.json()
                        member_data = data['guild']['members']
                        total_members = len(member_data)
                        guild_name = data['guild']['name']
                        try:
                            guild_tag = f" [{data['guild']['tag']}]"
                        except KeyError:
                            guild_tag = ""
                        formatted_member_info = []      
                        
                        # Sort members by GEXP points in descending order
                        member_data.sort(key=lambda member: member['expHistory'].get(yesterday_date, 0), reverse=True)
                        
                        self.total_points = 0
                        
                        for member in member_data:
                            #print(member['uuid'], member['expHistory'][yesterday_date])
                            self.total_points += member['expHistory'][yesterday_date]
                            
                        #print(f"Full total GEXP: {self.total_points}")

                        max_contributors = 30
                        max_contributors = min(max_contributors, len(member_data))  # Ensure max_contributors is within the list size
                        total_contributors = 0
                        
                        
                        formatted_member_info = []  # Create an empty list

                        for i, member in enumerate(member_data[:max_contributors], start=1):
                            user_uuid = member['uuid']
                            experience = member['expHistory'].get(yesterday_date, 0)
                            
                            # Check if the UUID matches a verified account and format the user string
                            discord_id = None
                            for discord_user_id, account_data in verified_accounts.items():
                                if account_data.get('uuid') == user_uuid:
                                    discord_id = discord_user_id
                                    break
                                
                            uuid = user_uuid
                            user_name = search_uuid_and_return_name("guild_cache.json", uuid)
                            
                            if user_name == None:
                                user_name = "Still loading member data..."
                            else:
                                pass
                            
                            if experience > 0:
                                total_contributors += 1

                            if discord_id:
                                formatted_info = f"#{str(i).zfill(2)}. - {user_name} - {'{:,}'.format(experience)}"
                            else:
                                formatted_info = f"#{str(i).zfill(2)}. - {user_name} - {'{:,}'.format(experience)}"

                            formatted_member_info.append(formatted_info)
                
                    background_image = Image.open("./assets/backgrounds/810_670.png")
                    overlay_image = Image.open("./assets/overlays/guild_points_top.png")
                        
                    background_image.paste(overlay_image, (0, 0), overlay_image)
                    
                    text1 = f"{guild_name}{guild_tag} - Daily GEXP"
                    text2 = f"© {guild.name}"
                    text3 = f"Total:  {'{:,}'.format(self.total_points)}       Contributors: {total_contributors}/{total_members}       Average:  {(self.total_points / total_members):.1f}"
                    
                    draw = ImageDraw.Draw(background_image)
                    
                    _, _, text1_width, _ = draw.textbbox((0, 0), text1, font=font_title)
                    _, _, text2_width, _ = draw.textbbox((0, 0), text2, font=font_footer)
                    _, _, text3_width, _ = draw.textbbox((0, 0), text3, font=font_footer)
                    
                    image_width, _ = background_image.size
                    center_x1 = (image_width - text1_width) // 2
                    center_x2 = (image_width - text2_width) // 2
                    center_x3 = (image_width - text3_width) // 2
                    
                    draw = ImageDraw.Draw(background_image)
                    draw.text((center_x1,20), text1, (85, 255, 85), font=font_title)
                    draw.text((center_x2,636), text2, (255, 255, 255), font=font_footer)
                    draw.text((center_x3,70), text3, (85, 255, 85), font=font_footer)

                    # Define the starting positions for the left and right columns
                    left_column_x = 25
                    right_column_x = 420
                    starting_y = 107  # Adjust this value as needed

                    # Define colors for the different parts of the text
                    index_color = (255, 255, 85)  # Red
                    username_color = (255, 255, 255)  # Green
                    experience_color = (255, 255, 85)  # Blue

                    # Iterate through the usernames and draw them with different colors
                    for i, formatted_info in enumerate(formatted_member_info, start=1):
                        x = left_column_x if i <= 15 else right_column_x
                        y = starting_y + (i - 1) % 15 * 35  # 30px spacing

                        # Split the formatted_info into parts
                        parts = formatted_info.split(" - ")
                        
                        
                        # Draw each part with a specific color
                        draw.text((x, y), f"#{str(i).zfill(2)}.", index_color, font=font_username)
                        draw.text((x + 40, y), parts[1], username_color, font=font_username)
                        draw.text((center((x + 320), parts[2], font_username), y), parts[2], experience_color, font=font_username)
                    
                    background_image.save("./assets/outputs/guild_daily_top.png") # save the img
                    await channel.send(file=discord.File("./assets/outputs/guild_daily_top.png"))
                    
                    already_sent = True
                else:
                    pass
            else:
                already_sent = False
        else:
            pass
        
        
async def setup(client):
    await client.add_cog(dailygpoints(client))