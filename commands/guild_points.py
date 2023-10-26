import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import json
import discord
import requests
import discord.ui
import os
from dotenv import load_dotenv
import asyncio
import time
import pytz
import utils.guild_data as guild

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
hypixel_guild_id = data["hypixel_ids"]["guild_id"]


class guildPointsCMD(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.guild_id = hypixel_guild_id
    
    @commands.hybrid_command(aliases = ["dgp", "gexp"], brief="guildpoints", description="Shows the current top GEXP contributors", with_app_command=True)
    @commands.cooldown(1, 120, commands.BucketType.user) # 2 min cool down.
    async def guildpoints(self, ctx):
        
        # Define the Eastern Time Zone
        eastern = pytz.timezone('US/Eastern')

        # Get the current time in the Eastern Time Zone
        current_time = datetime.now(eastern)

        # Format the date as "YYYY-MM-DD"
        formatted_date = current_time.strftime('%Y-%m-%d')
        
        
        try:
            # Load the "verified_accounts.json" file as a dictionary
            with open('verified_accounts.json', 'r') as verified_file:
                verified_accounts = json.load(verified_file)
                
            yesterday_date = formatted_date # this is just todays date EST
            # print(yesterday_date)
            hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
            api_link = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
            response = requests.get(api_link)

            if response.status_code == 200:
                data = response.json()
                member_data = data['guild']['members']
                guild_name = data['guild']['name']
                try:
                    guild_tag = f" [{data['guild']['tag']}]"
                except KeyError:
                    guild_tag = ""
                formatted_member_info = []
                
                await ctx.send(f"Now fetching {guild_name}'s data. This could take up to 1 minute.")

                # Sort members by GEXP points in descending order
                member_data.sort(key=lambda member: member['expHistory'].get(yesterday_date, 0), reverse=True)
                
                self.total_points = 0
                
                for member in member_data:
                    #print(member['uuid'], member['expHistory'][yesterday_date])
                    self.total_points += member['expHistory'][yesterday_date]
                    
                #print(f"Full total GEXP: {self.total_points}")

                max_contributors = 25
                max_contributors = min(max_contributors, len(member_data))  # Ensure max_contributors is within the list size
                
                # Record the start time
                start_time = time.time()

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
                    user_name = guild.search_uuid_and_return_name("guild_cache.json", uuid)
                    
                    if user_name == None:
                        user_name = uuid
                    else:
                        pass

                    if discord_id:
                        formatted_info = f"**{i}.** [{user_name} ✓](https://plancke.io/hypixel/player/stats/{user_uuid}) - **{experience}** GEXP"
                    else:
                        formatted_info = f"**{i}.** [{user_name}](https://plancke.io/hypixel/player/stats/{user_uuid}) - **{experience}** GEXP"

                    # print(formatted_info)
                    formatted_member_info.append(formatted_info)

                # this will go into effect if your Ensure max_contributors is within the list size
                # max contributors variable is OFF or commented out. Otherwise you can ignore.
                while len(formatted_member_info) < max_contributors:
                    i = len(formatted_member_info) + 1
                    formatted_info = f"**{i}.** Empty Member Slot - **0** GEXP"
                    formatted_member_info.append(formatted_info)

                formatted_member_string = ' \n '.join(formatted_member_info)
                #print(formatted_member_string)
                
                # Record the end time
                end_time = time.time()
                # Calculate the elapsed time
                elapsed_time = end_time - start_time
                #print(f"Elapsed time: {elapsed_time:.2f} seconds")
                
                embed = discord.Embed(
                    title = f"**🏆 | {guild_name}{guild_tag} Daily GEXP**", 
                    description=f"""
                    Today's total GEXP earned so far: **{format(self.total_points, ",")}**.
                    
                    **Top {max_contributors} GEXP Contributors:**
                    {formatted_member_string}
                    
                    Hypixel GEXP resets every 24 hours at 12AM EST.
                    """,
                    colour = embed_color
                    )
                #embed.set_thumbnail(url = "{}".format(ctx.guild.icon.url)),
                embed.timestamp = datetime.now()
                embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                await ctx.send(embed=embed)
            
        except Exception as e:
            error_message = str(e)
            await ctx.send(f"There was an error: {error_message}. Please double-check your Guild ID and Hypixel API key.")

        
async def setup(client):
    await client.add_cog(guildPointsCMD(client))
    

