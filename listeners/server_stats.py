import discord
from discord.ext import tasks, commands
import json
import discord.ui
import requests
import os

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

enable_feature = bool(data["features"]["server_stats"])
hypixel_guild_id = data["hypixel_ids"]["guild_id"]


# json data to get channel IDs
command_prefix = data["general"]["bot_prefix"]
member_role_id = int(data["role_ids"]["unverified_member"])
member_count_chanel_id = int(data["voice_channel_ids"]["member_count"])
members_online_channel_id = int(data["voice_channel_ids"]["members_online"])
guild_member_online_channel_id = int(data["voice_channel_ids"]["guild_member_online"])


# global variables for channel name usage
global_member_count = 0
global_online_members = 0
global_online_and_guild_member = 0


class serverstats(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.serverstats.start()


    @tasks.loop(seconds=600.0)  # runs every 10 minutes to avoid being rate limited
    async def serverstats(self):
        
        try:
            hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
            
            api_link = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
            response = requests.get(api_link)
            data = response.json()
            
            
            guild_data = data['guild']
            total_guild_members = len(guild_data['members'])
            
        except:
            total_guild_members = "NA"

        # Open the JSON file and read in the data
        with open('config.json') as json_file:
            data = json.load(json_file)

        enable_feature = bool(data["features"]["server_stats"])


        #json data to get channel IDs
        member_count_chanel_id = data["voice_channel_ids"]["member_count"]
        members_online_channel_id = data["voice_channel_ids"]["members_online"]
        guild_member_online_channel_id = data["voice_channel_ids"]["guild_member_online"]
        guild_member_role_id = int(data["role_ids"]["guild_member"])

        #if the feature is enabled then it will run
        if enable_feature:

            member_count_channel = self.client.get_channel(int(member_count_chanel_id)) #ID of voice channel that changes
            members_online_channel = self.client.get_channel(int(members_online_channel_id)) #ID of voice channel online members
            guild_member_online_channel = self.client.get_channel(int(guild_member_online_channel_id)) #guild_member online voice channel

            #if a change has been detected.
            #this helps with being rate limited by discord

            member_count = len(self.client.guilds[0].members)
            global global_member_count
            if (global_member_count != member_count):
                global_member_count = member_count
                try:
                    await member_count_channel.edit(name=f"Member Count: {member_count}")
                except:
                    pass # means we got rated limited so try again in 5 min
            else:
                pass

            online_members = [member for member in self.client.guilds[0].members if member.status != discord.Status.offline]
            global global_online_members
            if (global_online_members != online_members):
                global_online_members = online_members
                try:
                    await members_online_channel.edit(name=f"Online Users: {len(online_members)}")
                except:
                    pass # means we got rated limited so try again in 5 min
            else:
                pass

            global global_online_and_guild_member
            if (global_online_and_guild_member != total_guild_members):
                global_online_and_guild_member = total_guild_members
                try:
                    await guild_member_online_channel.edit(name=f"Guild Members {total_guild_members}/125")
                except:
                    pass # means we got rated limited so try again in 5 min
            else:
                pass

        else:
            pass


async def setup(client):
    await client.add_cog(serverstats(client))