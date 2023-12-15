import discord
from discord.ext import tasks, commands
import json
import discord.ui
import requests
import os
import asyncio
import datetime

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

guild_id = int(data["general"]["discord_server_guild_id"])
logs_channel_id = int(data["text_channel_ids"]["guild_news"])    # logs the bot logs in this channel
embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

hypixel_guild_id = data["hypixel_ids"]["guild_id"]
hypixel_api_key = os.getenv("HYPIXEL_API_KEY")



class guildMemberCacher(commands.Cog):

    def __init__(self, client):
        self.guild_id = guild_id
        self.client = client
        # Load existing guild_member_data from JSON file
        try:
            with open('guild_cache.json', 'r') as file:
                self.guild_member_data = json.load(file)
        except FileNotFoundError:
            self.guild_member_data = {}  # Initialize an empty dictionary if the file doesn't exist
        self.guildMemberCacher.start()


    @tasks.loop(seconds=120)  # 2 players in 2 minutes (1 player per min).
    async def guildMemberCacher(self):
        # print("Loop Started")
        # guild = self.client.get_guild(self.guild_id)
        try:
            api_link = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
            response = requests.get(api_link)
            #print(response.status_code)

            if response.status_code == 200:
                data = response.json()
                members = data['guild']['members']
                total_guild_members = len(data['guild']['members'])

                # Load existing guild_member_data from JSON file
                try:
                    with open('guild_cache.json', 'r') as file:
                        guild_member_data = json.load(file)
                except FileNotFoundError:
                    guild_member_data = {"usernames": {}, "guild_data": {}}  # Initialize an empty dictionary if the file doesn't exist
                    
                # adds the api response to the guild data section
                guild_member_data["guild_data"] = data

                # Create a list of UUIDs from the API response
                api_uuids = [member["uuid"] for member in members]
                
                # Create a list of UUIDs to remove
                uuids_to_remove = []

                # Remove entries from guild_member_data if the UUID is not in api_uuids
                for uuid in guild_member_data["usernames"]:
                    if uuid not in api_uuids:
                        uuids_to_remove.append(uuid)
                        
                for uuid in uuids_to_remove:
                    # print(f"Removing {guild_member_data[uuid]} from the JSON.")
                    player_name = guild_member_data["usernames"][uuid]
                    del guild_member_data["usernames"][uuid]
                    
                    guild_member_cache_total = len(guild_member_data["usernames"])
                    
                    channel = self.client.get_channel(logs_channel_id)
                    embed = discord.Embed(
                        title=(f"😭 | {player_name} left/got kicked the guild."),
                        description=f"Player `{player_name}` has been removed from the guild data because they either left the guild or was kicked.\n\n **Total Guild Members: `{guild_member_cache_total}`/`125`**",
                        colour= embed_color
                    )
                    # embed.timestamp = datetime.datetime.now()
                    embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/{uuid}.png?y=-40")
                    # embed.set_footer(text=f"©️ {guild.name}", icon_url = guild.icon.url)
                    
                    await channel.send(embed=embed)

                member_counter = 0  # Counter for added members in the current loop iteration

                for member in members:
                    if member_counter >= 2:
                        break  # Pause adding members when the limit is reached

                    uuid = member["uuid"]

                    # Add member data to the guild_member_data dictionary if it's not a duplicate
                    if uuid not in guild_member_data["usernames"]:
                        await asyncio.sleep(0.25)
                        username_url = f'https://api.mojang.com/user/profile/{uuid}'
                        ign_response = requests.get(username_url)
                        if ign_response.status_code == 200:
                            ign = ign_response.json()['name']
                        else:
                            ign = "Username Not Found"  # if API fails
                        guild_member_data["usernames"][uuid] = ign
                        #print(f"{ign} has been added!")
                        
                        guild_member_cache_total = len(guild_member_data["usernames"])
                        # print(f"Total: {guild_member_cache_total}")
                        
                        
                        channel = self.client.get_channel(logs_channel_id)
                        embed = discord.Embed(
                            title=(f"😊 | {ign} has just joined the guild!"),
                            description=f"Player `{ign}` was just loaded into the guild cache. This means that they either just joined or was just now loaded. Their username will now appear in all guild commands.\n\n **Total Guild Members: `{guild_member_cache_total}`/`125`**",
                            colour= embed_color
                        )
                        # embed.timestamp = datetime.datetime.now()
                        embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/{uuid}.png?y=-40")
                        # embed.set_footer(text=f"©️ {guild.name}", icon_url = guild.icon.url)
                        
                        await channel.send(embed=embed)

                        member_counter += 1  # Increment the member counter

                    # Save the updated data to the JSON file at the end of the loop
                    with open('guild_cache.json', 'w') as file:
                        json.dump(guild_member_data, file, indent=2)
            else:
                pass

        except Exception as e:
            # Handle the exception and print the error message
            print(f"An error occurred: {e}")

async def setup(client):
    await client.add_cog(guildMemberCacher(client))