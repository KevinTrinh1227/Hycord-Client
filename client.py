import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext import tasks
import requests
import discord.ui
import asyncio
import datetime
import os
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

#json data to get channel IDs
welcome_channel_id = int(data["welcome_channel_id"])
member_role_id = int(data["basic_member_role_id"])
member_count_chanel_id = int(data["member_count_chanel_id"])
members_online_channel_id = int(data["members_online_channel_id"])
guild_member_online_channel_id = int(data["guild_member_online_channel_id"])
sweat_role_id = int(data["sweat_role_id"])

#global variables for channel name usage
global_member_count = 0
global_online_members = 0
global_online_and_sweaty = 0

def activateBot (discord_bot_token, bot_prefix, embed_color):
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix = bot_prefix, case_insensitive=True, intents=intents)
    client.remove_command("help") #removes the default help command
    
    
    #startup event on_ready
    @client.event
    async def on_ready():
        name = client.user.name.upper()
        discriminator = client.user.discriminator.upper()
        print(f"\nNOW ACTIVATING: {name}#{discriminator}")
        print("===========================================")    
        await load_cogs()
        print (f"{os.path.basename(__file__):<20}{'Successfully loaded ✅':<30}")
        print("===========================================\n")
        change_stats_channels.start()
        
        
    #2 channel names changes per 10 minutes (1 every 5 mins)
    @tasks.loop(seconds=301.0) #refreshes every x seconds + 1 second to avoid warning
    async def change_stats_channels():
        
        member_count_channel = client.get_channel(member_count_chanel_id) #ID of voice channel that changes
        members_online_channel = client.get_channel(members_online_channel_id) #ID of voice channel online members
        guild_member_online_channel = client.get_channel(guild_member_online_channel_id) #guild_member online voice channel
        sweaty_role = discord.utils.get(client.guilds[0].roles, id=sweat_role_id)
    
    
        #if a change has been detected.
        #this helps with being rate limited by discord
        
        member_count = len(client.guilds[0].members)
        global global_member_count
        if (global_member_count != member_count):
            global_member_count = member_count
            await member_count_channel.edit(name=f"Member Count: {member_count}")
        else:
            pass
        
        online_members = [member for member in client.guilds[0].members if member.status != discord.Status.offline]
        global global_online_members
        if (global_online_members != online_members):
            global_online_members = online_members
            await members_online_channel.edit(name=f"Online Members: {len(online_members)}")
        else:
            pass
        
        online_and_sweaty_members = [member for member in client.guilds[0].members if sweaty_role in member.roles and member.status != discord.Status.offline]
        global global_online_and_sweaty
        if (global_online_and_sweaty != online_and_sweaty_members):
            global_online_and_sweaty = online_and_sweaty_members
            await guild_member_online_channel.edit(name=f"Guild Online: {len(online_and_sweaty_members)}/125")
        else:
            pass
        
            
            
    #on member join event        
    @client.event
    async def on_member_join(member):
        #Auto role feature
        role = member.guild.get_role(member_role_id) #ID of normal member role
        roleStr = str(role)
        autoRole = discord.utils.get(member.guild.roles, name = roleStr)
        await member.add_roles(autoRole)
        #welcome embed
        member_count = len(member.guild.members)
        channel = client.get_channel(welcome_channel_id)
        embed = discord.Embed(
            title=(f"Welcome to {member.guild.name} (#{member_count})"),
            description = f"Welcome to the Sweaty Sanctum's Community! Link/verify your account using `!link [your IGN]`.\n\nMember: {member.mention} \n\n**Verify Account ➜** <#1057045238729953412> \n**Information ➜** <#934776549717184552> \n**Select Roles ➜** <#934418278888144906> \n",
            colour= embed_color
            )
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url = "{}".format(member.avatar.url))
        embed.set_image(url="https://imgur.com/btR7AnN.png")
        embed.set_footer(text=f"©️ {member.guild.name}", icon_url = member.guild.icon.url)
        await channel.send(f"||{member.mention}||")
        await channel.purge(limit = 1)
        await channel.send(embed=embed)
        
        
    async def load_cogs():
        #load in all listeners
        print(f"{'LISTENER FILES':<20}{'LOAD STATUS':<30}")
        for filename in os.listdir("./listeners"):
            if filename.endswith(".py"):
                await client.load_extension(f"listeners.{filename[:-3]}")
                print (f"{filename:<20}{'Successfully loaded ✅':<30}")
        print(f"\n{'COMMAND FILES':<20}{'LOAD STATUS':<30}")
        #load in all commands
        for filename in os.listdir("./commands"):
            if filename.endswith(".py"):
                await client.load_extension(f"commands.{filename[:-3]}")
                print (f"{filename:<20}{'Successfully loaded ✅':<30}")
        print(f"\n{'OTHER FILES':<20}{'LOAD STATUS':<30}")
    
    
    client.run(discord_bot_token)
        