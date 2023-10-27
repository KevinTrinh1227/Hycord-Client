import discord
from discord.ext import tasks, commands
import json
import discord.ui
import requests
import os
import asyncio

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

hypixel_guild_id = data["hypixel_ids"]["guild_id"]
hypixel_api_key = os.getenv("HYPIXEL_API_KEY")



class guildMemberCacher(commands.Cog):

    def __init__(self, client):
        self.client = client
        # Load existing guild_member_data from JSON file
        try:
            with open('guild_cache.json', 'r') as file:
                self.guild_member_data = json.load(file)
        except FileNotFoundError:
            self.guild_member_data = {}  # Initialize an empty dictionary if the file doesn't exist
        self.guildMemberCacher.start()


    @tasks.loop(seconds=120)  # 2 players in 2 minutes (1 player per min)
    async def guildMemberCacher(self):
        #print("Loop Started")
        try:
            api_link = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
            response = requests.get(api_link)
            #print(response.status_code)

            if response.status_code == 200:
                data = response.json()
                members = data['guild']['members']

                # Load existing guild_member_data from JSON file
                try:
                    with open('guild_cache.json', 'r') as file:
                        guild_member_data = json.load(file)
                except FileNotFoundError:
                    guild_member_data = {}  # Initialize an empty dictionary if the file doesn't exist

                # Create a list of UUIDs from the API response
                api_uuids = [member["uuid"] for member in members]

                # Remove entries from guild_member_data if the UUID is not in api_uuids
                for uuid in list(guild_member_data.keys()):
                    if uuid not in api_uuids:
                        #print(f"Removing {guild_member_data[uuid]} from the JSON.")
                        del guild_member_data[uuid]

                member_counter = 0  # Counter for added members in the current loop iteration

                for member in members:
                    if member_counter >= 2:
                        break  # Pause adding members when the limit is reached

                    uuid = member["uuid"]

                    # Add member data to the guild_member_data dictionary if it's not a duplicate
                    if uuid not in guild_member_data:
                        await asyncio.sleep(0.25)
                        username_url = f'https://api.mojang.com/user/profile/{uuid}'
                        ign_response = requests.get(username_url)
                        if ign_response.status_code == 200:
                            ign = ign_response.json()['name']
                        else:
                            ign = "Username Not Found"  # if API fails
                        guild_member_data[uuid] = ign
                        #print(f"{ign} has been added!")

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