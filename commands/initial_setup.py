import discord
from discord.ext import commands
import requests
import discord.ui
import asyncio
import datetime
import os
from dotenv import load_dotenv
import json
from discord import app_commands


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    
    
class initialsetup(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.has_permissions(administrator = True)
    @commands.hybrid_command(aliases=["botsetup"], pass_context=True, brief="setup", description="Setup the bot configurations", with_app_command=True)
    async def setup(self, ctx):
        
        # Read the existing config.json file
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            
        if config["config"]["bool"] == 0:

            try:

                guild = ctx.guild

                # timeout timer for when it stops
                timeout_time_in_seconds = 60

                # General bot prefix
                await ctx.send("Enter a bot command prefix (e.g., `.`):")
                chosen_command_prefix = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['general']['bot_prefix'] = chosen_command_prefix.content

                # General embed color
                await ctx.send("Enter the embed color (in hex format, e.g., #ff0000 for red):")
                chosen_hex_color = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['general']['embed_color'] = chosen_hex_color.content

                
                # General discord guild ID
                guild_id = ctx.guild.id
                config["general"]["discord_server_guild_id"] = str(guild_id)


                # Server Stats
                await ctx.send("Enable server stats? (0 for No, 1 for Yes):")
                server_stats = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=timeout_time_in_seconds)
                config['features']['server_stats'] = int(server_stats.content)
                # the server stats category and channels will be generated at the end of the setup process
                    
                
                # Daily GEXP annoucements
                await ctx.send("Enable daily guild gexp announcements? This will send the top GEXP players in your guild in a specified channel. (0 for No, 1 for Yes):")
                auto_gexp = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=timeout_time_in_seconds)
                config['features']['auto_daily_gexp'] = int(auto_gexp.content)
                    
                # Coins & level system question
                await ctx.send("Enable chat coin and level system? (0 for No, 1 for Yes):")
                filtered_chat = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['coin_level_system'] = int(filtered_chat.content)

                # Filtered chat
                await ctx.send("Enable filtered chat? (0 for No, 1 for Yes):")
                filtered_chat = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['filtered_chat'] = int(filtered_chat.content)


                # Inactivity command
                await ctx.send("Enable inactivity command? This command will allow guild members only to share a time frame where they will be inactive for in a specific channel. (0 for No, 1 for Yes):")
                inactivity_cmd = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['inactivity_cmd'] = int(inactivity_cmd.content)

                # Punishments command
                await ctx.send("Enable punishments command? (0 for No, 1 for Yes):")
                punishments_cmd = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['punishments_cmd'] = int(punishments_cmd.content)


                # Welcome channel
                await ctx.send("Reference your welcome channel (Mention the channel by using #<channel name>):")
                welcome_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                welcome_channel_id = welcome_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['welcome'] = str(welcome_channel_id)
                
                # If auto gexp is on
                if auto_gexp.content == "0":
                    config['text_channel_ids']['daily_guild_points'] = 0
                else:
                    # Daily guild points channel
                    await ctx.send("Reference your daily guild points channel where the daily top GEXP message will be sent to. (Reference the channel by using #<channel name>):")
                    daily_guild_points_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                    daily_guild_points_channel_id = daily_guild_points_channel_mention.channel_mentions[0].id
                    config['text_channel_ids']['daily_guild_points'] = str(daily_guild_points_channel_id)

                # If the user said 0 or no for the inactivity command, set the inactivity channel to "0" and don't ask to reference the inactivity command
                if inactivity_cmd.content == "0":
                    config['text_channel_ids']['inactivity_notice'] = 0
                else:
                    # Inactivity notice channel
                    await ctx.send("Reference your inactivity notice channel (Reference the channel by using #<channel name>):")
                    inactivity_notice_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=timeout_time_in_seconds)
                    inactivity_notice_channel_id = inactivity_notice_channel_mention.channel_mentions[0].id
                    config['text_channel_ids']['inactivity_notice'] = str(inactivity_notice_channel_id)

                # Staff chat channel
                await ctx.send("Reference your bot logs channel. (Reference the channel by using #<channel name>):")
                bot_logs_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                bot_logs_channel_id = bot_logs_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['bot_logs'] = str(bot_logs_channel_id)

                # Tickets transcripts channel
                await ctx.send("Reference your tickets transcripts channel (Reference the channel by using #<channel name>):")
                tickets_transcripts_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                tickets_transcripts_channel_id = tickets_transcripts_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['tickets_transcripts'] = str(tickets_transcripts_channel_id)


                # Guild member role
                await ctx.send("Reference the guild member role (Mention the role by using @<role name>):")
                guild_member_role_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                guild_member_role_id = guild_member_role_mention.role_mentions[0].id
                config['role_ids']['guild_member'] = str(guild_member_role_id)

                # Verified member role
                await ctx.send("Reference the verified member role (Mention the role by using @<role name>):")
                verified_member_role_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                verified_member_role_id = verified_member_role_mention.role_mentions[0].id
                config['role_ids']['verified_member'] = str(verified_member_role_id)

                # Unverified member role
                await ctx.send("Reference the unverified member role (Mention the role by using @<role name>):")
                unverified_member_role_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                unverified_member_role_id = unverified_member_role_mention.role_mentions[0].id
                config['role_ids']['unverified_member'] = str(unverified_member_role_id)

                # Staff member role
                await ctx.send("Reference the staff member role (Mention the role by using @<role name>):")
                staff_member_role_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                staff_member_role_id = staff_member_role_mention.role_mentions[0].id
                config['role_ids']['staff_member'] = str(staff_member_role_id)

                # Getting the Hypixel Guild ID
                await ctx.send("Enter an IGN of a member that is inside your guild so the bot can retrieve your guild ID:")
                guild_member = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)

                #load in .env variables
                load_dotenv() 

                #get hypixel api key
                hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
                

                url = f"https://api.mojang.com/users/profiles/minecraft/{guild_member.content}?"
                response = requests.get(url)
                uuid = response.json()['id']


                #user guild information
                guild_url = f"https://api.hypixel.net/guild?player={uuid}&key={hypixel_api_key}"
                guild_response = requests.get(guild_url)
                guild_data = guild_response.json()


                #checks if user is in a guild
                try:
                    if "name" in guild_data["guild"]:
                        guild_name = guild_data["guild"]["name"]
                        guild_id = guild_data["guild"]["_id"]
                        #print(f"Guild name: {guild_name}, with guild ID: {guild_id}")
                        await ctx.send(f"Discord server is now linked to Guild: `{guild_name}` with ID: `{guild_id}`.")
                    else:
                        guild_name = "Not in Guild"
                except: #runs if player is not in a guild
                    guild_name = "No Guild"
                    guild_id = "IGN_WAS_NOT_IN_GUILD"
                    print(f"Guild name: {guild_name}, with guild ID: {guild_id}")

                # set the string of hypixel guild ID
                config['hypixel_ids']['guild_id'] = str(guild_id)
                
                
                
                # Tickets category created last when intial config is done
                guild = ctx.guild
                category = await guild.create_category("TICKETS")
                # print(f"Category ID: {category.id}")
                config['category_ids']['tickets_category'] = category.id


                # creates the server stats channels
                try:
                    if server_stats.content == "1":
                        # Create the category
                        category = await guild.create_category('SERVER INFO')

                        # Get the total member count
                        total_member_count = len(guild.members)

                        # Get the number of online members
                        online_member_count = len(
                            [member for member in guild.members if member.status != discord.Status.offline])

                        # Get the guild_member_role_id from data["role_ids"]["guild_member"]
                        guild_member_role_id_str = data["role_ids"]["guild_member"]

                        if guild_member_role_id_str:
                            guild_member_role_id = int(guild_member_role_id_str)
                        else:
                            # Handle the case when the string is empty (e.g., set a default value)
                            guild_member_role_id = 0  # You can change the default value as needed

                        # Get the number of guild members with the specified role
                        guild_member_count = len([member for member in guild.members if
                                                  guild_member_role_id in [role.id for role in member.roles]])

                        # Create voice channels with dynamic names
                        channel_names = [
                            f'Member Count: {total_member_count}',
                            f'Online Users: {online_member_count}',
                            f'Guild Members: {guild_member_count}/125'
                        ]

                        voice_channel_ids = {
                            'member_count': '',
                            'members_online': '',
                            'guild_member_online': ''
                        }

                        for channel_name in channel_names:
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(connect=False)
                            }
                            channel = await guild.create_voice_channel(channel_name, overwrites=overwrites,
                                                                       category=category)
                            print(f'Channels Created: {channel.name} - {channel.id}')

                            # Update the voice_channel_ids dictionary with the correct channel ID
                            if 'Member Count' in channel_name:
                                voice_channel_ids['member_count'] = str(channel.id)
                            elif 'Online Users' in channel_name:
                                voice_channel_ids['members_online'] = str(channel.id)
                            elif 'Guild Members' in channel_name:
                                voice_channel_ids['guild_member_online'] = str(channel.id)
                    else:
                        # User chose not to enable server stats, set default IDs to 0
                        voice_channel_ids = {
                            'member_count': '0',
                            'members_online': '0',
                            'guild_member_online': '0'
                        }
                except Exception as e:
                    print(f"ERROR: {e}")

                # Update the voice channel data
                config['voice_channel_ids'].update(voice_channel_ids)



                # sets the config bool to 1 aka True so that means that
                # the bot has already been setup and no longer requires
                # a configuration anymore.
                config["config"]["bool"] = 1


                # Save the updated config to config.json
                with open('config.json', 'w') as config_file:
                    json.dump(config, config_file, indent=2)


                # saves all the data we just got to the config.json
                await ctx.send("Configuration settings updated successfully. 🟢")
                await ctx.send("You must **RESTART** your bot again for it to work! ⚠️ ")
                
                # prints to console as well
                print("\n\n----------------------------------------------------------")
                for i in range(0, 10):
                    print("* YOUR BOT NOW REQUIRES A RESTART FOR UPDATES TO TAKE EFFECT.")
                print("----------------------------------------------------------")
                
                
            # means that the use did not give us data in time
            except:
                await ctx.send("No response received. Please try again.")
                
            
        else:
            await ctx.send("This bot has already been through the intial setup.")

        
        
async def setup(client):
    await client.add_cog(initialsetup(client))