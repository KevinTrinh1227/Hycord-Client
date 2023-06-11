import discord
from discord.ext import tasks, commands
import datetime
import json
import pytz
import discord
import requests
import discord.ui
import os
from dotenv import load_dotenv

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

enable_feature = bool(data["features"]["auto_gexp"])

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
hypixel_guild_id = data["hypixel_ids"]["guild_id"]
daily_points_channel_id = int(data["text_channel_ids"]["daily_guild_points"])
guild_id = int(data["general"]["discord_server_guild_id"])
command_prefix = data["general"]["bot_prefix"]

already_sent = False

class dailygpoints(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.guild_id = guild_id
        self.dailygpoints.start()
    
    
    @tasks.loop(seconds=10.0)
    async def dailygpoints(self):

        """
        print(enable_feature)
        print(type(enable_feature))
        """

        #if the feature is enabled then it will run
        if enable_feature:
        
            channel = self.client.get_channel(daily_points_channel_id)
            
            global already_sent #checks whether we already sent message or not
            
            est = pytz.timezone('US/Eastern')
            current_time = datetime.datetime.now(est)
            
            #sends when it is 11:55 EST in 24 hour time format is 23:55
            if current_time.hour == 23 and current_time.minute == 55:
            #if 1 == 1:
                #print("It is currently 11:59pm in Eastern Standard Time (EST)")
                #print(f"Current time in EST: {current_time.strftime('%I:%M %p')}")
                #print(f"Current hour: {current_time.hour}")
                #print(f"Current minute: {current_time.minute}")
                
                if already_sent == False:
                    hypixel_api_key = os.getenv("HYPIXEL_API_KEY")

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
                    
                    guild = self.client.get_guild(self.guild_id)
                    guild_icon_url = guild.icon.url
                    
                    embed = discord.Embed(
                        title = f"**{guild_name}'s Daily Guild Points**", 
                        description=f"A total of `{total_exp}` was earned today! Daily top resets everyday at Midnight EST. Please use `{command_prefix}dgp` to see current guild points.\n```{embed_string}```",
                        colour = embed_color
                    )
                    embed.set_thumbnail(url = guild_icon_url),
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text=f"©️ {guild.name}", icon_url = guild_icon_url)
                    await channel.send(embed=embed)
                    already_sent = True
                else:
                    #print("Will not send cause already sent embem. Boolean is...")
                    #print(already_sent)
                    pass
                
            else:
                #print("It is not currently 11:59pm in Eastern Standard Time (EST)")
                #print(f"Current time in EST: {current_time.strftime('%I:%M %p')}")
                #print(f"Current hour: {current_time.hour}")
                #print(f"Current minute: {current_time.minute}")
                already_sent = False
                #print(already_sent)
                #pass
    
        #if feature is disabled in config we ignore
        else:
            pass
        
        
async def setup(client):
    await client.add_cog(dailygpoints(client))