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
import traceback


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
                await ctx.send("Enter a bot prefix you would like your bot to use. Note that all commands are hybrid, meaning they will work with either prefix or with a `/`. Some examples: `?`, `.`, `!`.")
                chosen_command_prefix = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['general']['bot_prefix'] = chosen_command_prefix.content

                # General embed color
                await ctx.send("Enter a primary color in HEX format (e.g., #ff0000 for bright red). This color will be used as all your embed colors.")
                chosen_hex_color = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['general']['embed_color'] = chosen_hex_color.content

                
                # General discord guild ID
                guild_id = ctx.guild.id
                config["general"]["discord_server_guild_id"] = str(guild_id)


                # Server Stats
                await ctx.send("Enable the server stats channels? These channels will update every 10 minutes with your member count, guild member online count, etc. (0 for No, 1 for Yes)")
                server_stats = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=timeout_time_in_seconds)
                config['features']['server_stats'] = int(server_stats.content)
                # the server stats category and channels will be generated at the end of the setup process
                    
                    
                # Coins & level system question
                await ctx.send("Enable chat coin and level system? This will reward members for chatting and participating in your server channels. (0 for No, 1 for Yes):")
                filtered_chat = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['coin_level_system'] = int(filtered_chat.content)
                
                # Auto GEXp feature
                await ctx.send("Enable auto GEXP feature? This feature will automatically send a daily guild points report of the top guild contributors in a specified channel. (0 for No, 1 for Yes):")
                auto_gexp_feature = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['auto_daily_gexp'] = int(auto_gexp_feature.content)

                # Filtered chat
                await ctx.send("Enable filtered chat? (0 for No, 1 for Yes):")
                filtered_chat = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['filtered_chat'] = int(filtered_chat.content)
                
                # Self selection roles
                await ctx.send("Enable self selection roles? This will allow users to select their own public roles from a list of roles you provide in a bit. Remember that you can always edit the description, title, roles labels, etc all inside the `config.json`. (0 for No, 1 for Yes")
                self_roles = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                if self_roles.content == '1':
                    await ctx.send("How many roles would you like to add to the menu? Please enter an integer number.")
                    roles_count = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=timeout_time_in_seconds)
                    list_of_roles = []

                    for i in range(int(roles_count.content)):
                        await ctx.send(f"Enter the label for role #{i + 1}. Note that this label will be used as the button label, so you can either only enter an emoji, or the emoji + name of the role, etc.")
                        label_message = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=timeout_time_in_seconds)
                        role_label = label_message.content

                        await ctx.send(f"Reference the role for {role_label} (Mention the role by using @<role name>):")
                        role_mention_message = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=timeout_time_in_seconds)
                        role_id = role_mention_message.role_mentions[0].id

                        # Create a role object with label and role ID
                        role = {
                            "button_label": role_label,
                            "role_id": role_id
                        }

                        # Append this role to the list_of_roles
                        list_of_roles.append(role)

                    # Now, you can use the list_of_roles to construct your JSON object
                    config["embed_templates"]["selection_roles"]["list_of_roles"] = list_of_roles
                    print(list_of_roles)
                        
                    

                # Inactivity command
                await ctx.send("Enable inactivity command? This command will allow guild members only, to share a time frame where they will be inactive for, in a specific channel. (0 for No, 1 for Yes):")
                inactivity_cmd = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['inactivity_cmd'] = int(inactivity_cmd.content)

                # Punishments command
                await ctx.send("Enable punishments command? If you want to use a different bot for punishment commands, enter `0`. (0 for No, 1 for Yes):")
                punishments_cmd = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['punishments_cmd'] = int(punishments_cmd.content)


                # Welcome channel
                await ctx.send("Reference your welcome channel (Mention the channel by using #<channel name>):")
                welcome_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                welcome_channel_id = welcome_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['welcome'] = str(welcome_channel_id)

                # If the user said 0 or no for the inactivity command, set the inactivity channel to "0" and don't ask to reference the inactivity command
                if inactivity_cmd.content == "0":
                    config['text_channel_ids']['inactivity_notice'] = "0"
                else:
                    # Inactivity notice channel
                    await ctx.send("Reference your inactivity notice channel (Mention the channel by using #<channel name>):")
                    inactivity_notice_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=timeout_time_in_seconds)
                    inactivity_notice_channel_id = inactivity_notice_channel_mention.channel_mentions[0].id
                    config['text_channel_ids']['inactivity_notice'] = str(inactivity_notice_channel_id)

                # Staff chat channel
                await ctx.send("Reference your bot logs channel. All bot logs will be posted in this channel. (Mention the channel by using #<channel name>):")
                bot_logs_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                bot_logs_channel_id = bot_logs_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['bot_logs'] = str(bot_logs_channel_id)

                # guild news channel
                await ctx.send("Reference your guild news channel. This channel is where the bot will send messages when someone join/leaves your guild, guild level ups, etc. (Mention the channel by using #<channel name>):")
                guild_news_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                guild_news_channel_id = guild_news_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['guild_news'] = str(guild_news_channel_id)

                # Tickets transcripts channel
                await ctx.send("Reference your tickets transcripts channel. This channel will house all of your closed ticket reciepts for backup. Do Not Delete them. (Mention the channel by using #<channel name>):")
                tickets_transcripts_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                tickets_transcripts_channel_id = tickets_transcripts_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['tickets_transcripts'] = str(tickets_transcripts_channel_id)


                # Daily GEXP message channel
                if auto_gexp_feature.content == "0":
                    config['text_channel_ids']['daily_guild_points'] = "0"
                else:
                    await ctx.send("Reference your daily guild points channel (Mention the channel by using #<channel name>):")
                    daily_guild_points_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                    daily_guild_points_channel_id = daily_guild_points_channel_mention.channel_mentions[0].id
                    config['text_channel_ids']['daily_guild_points'] = str(daily_guild_points_channel_id)


                # Guild member role
                await ctx.send("Reference the guild member role. This is the role all guild members have. (Mention the role by using @<role name>):")
                guild_member_role_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                guild_member_role_id = guild_member_role_mention.role_mentions[0].id
                config['role_ids']['guild_member'] = str(guild_member_role_id)

                # Verified member role
                await ctx.send("Reference the verified member role. This role will be given to users that verify/link their Discord and Hypixel Minecraft accounts together. (Mention the role by using @<role name>):")
                verified_member_role_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                verified_member_role_id = verified_member_role_mention.role_mentions[0].id
                config['role_ids']['verified_member'] = str(verified_member_role_id)

                # Unverified member role
                await ctx.send("Reference the unverified member role. This is the default role all members will get when they first join your server. (Mention the role by using @<role name>):")
                unverified_member_role_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                unverified_member_role_id = unverified_member_role_mention.role_mentions[0].id
                config['role_ids']['unverified_member'] = str(unverified_member_role_id)

                # Staff member role
                await ctx.send("Reference the staff member role. Note that staff members will also be able to view support tickets. (Mention the role by using @<role name>):")
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


                await ctx.send("**IMPORTANT:** Remember that you you can always edit your settings, embed messages layout, and everything else inside the `config.json` file. If when you do, restart your bot/client for the new changes to take effect.")

                # saves all the data we just got to the config.json
                await ctx.send("Configuration settings updated successfully. 🟢")
                await ctx.send("You must **RESTART** your bot again for it to work! ⚠️ ")
                
                # prints to console as well
                print("\n\n----------------------------------------------------------")
                for i in range(0, 10):
                    print("* YOUR BOT NOW REQUIRES A RESTART FOR UPDATES TO TAKE EFFECT.")
                print("----------------------------------------------------------")
                
                
            # means that the use did not give us data in time
            except Exception as e:  # Capture the exception
                traceback.print_exc()  # Print the exception traceback
                await ctx.send(f"An exception occurred: {str(e)}")  # Send the exception message to the user
                await ctx.send("No response received. Please try again.")
                
            
        else:
            await ctx.send("This bot has already been through the intial setup.")

        
        
async def setup(client):
    await client.add_cog(initialsetup(client))