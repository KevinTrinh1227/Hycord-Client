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
                try:
                    server_stats = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=timeout_time_in_seconds)
                    config['features']['server_stats'] = int(server_stats.content)

                    if config['features']['server_stats'] == 1:
                        # Create the category
                        category = await guild.create_category('SERVER INFO')

                        # Create the locked channels under the category
                        channel_names = ['Member Count: ###', 'Online Members: ###', 'Guild Online: ##/###']
                        voice_channel_ids = {
                            'member_count': '',
                            'members_online': '',
                            'guild_member_online': ''
                        }
                        for channel_name in channel_names:
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(connect=False)
                            }
                            channel = await guild.create_voice_channel(channel_name, overwrites=overwrites, category=category)
                            print(f'Created channel: {channel.name} ({channel.id})')
                            for key in voice_channel_ids:
                                if voice_channel_ids[key] == '':
                                    voice_channel_ids[key] = str(channel.id)

                    else:
                        # User chose not to enable server stats, set default IDs to 0
                        voice_channel_ids = {
                            'member_count': '0',
                            'members_online': '0',
                            'guild_member_online': '0'
                        }

                    # update the voice channel data
                    config['voice_channel_ids'].update(voice_channel_ids)
                except asyncio.TimeoutError:
                    await ctx.send("Timed out. Please try again later.")
                    
                    
                # Coins & level system question
                await ctx.send("Enable chat coin and level system? (0 for No, 1 for Yes):")
                filtered_chat = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['coin_level_system'] = int(filtered_chat.content)

                # Filtered chat
                await ctx.send("Enable filtered chat? (0 for No, 1 for Yes):")
                filtered_chat = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['filtered_chat'] = int(filtered_chat.content)

                # Auto GEXP
                await ctx.send("Enable automatic GEXP daily messages? (0 for No, 1 for Yes):")
                auto_gexp = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                config['features']['auto_gexp'] = int(auto_gexp.content)

                # Inactivity command
                await ctx.send("Enable inactivity command? (0 for No, 1 for Yes):")
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

                # Rules channel
                await ctx.send("Reference your rules channel (Mention the channel by using #<channel name>):")
                rules_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                rules_channel_id = rules_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['rules'] = str(rules_channel_id)

                # Inactivity notice channel
                await ctx.send("Reference your inactivity notice channel (Mention the channel by using #<channel name>):")
                inactivity_notice_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                inactivity_notice_channel_id = inactivity_notice_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['inactivity_notice'] = str(inactivity_notice_channel_id)

                # Staff chat channel
                await ctx.send("Reference your staff chat channel (Mention the channel by using #<channel name>):")
                staff_chat_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                staff_chat_channel_id = staff_chat_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['staff_chat'] = str(staff_chat_channel_id)

                # Tickets transcripts channel
                await ctx.send("Reference your tickets transcripts channel (Mention the channel by using #<channel name>):")
                tickets_transcripts_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                tickets_transcripts_channel_id = tickets_transcripts_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['tickets_transcripts'] = str(tickets_transcripts_channel_id)

                # Leave messages channel
                await ctx.send("Reference your leave messages channel (Mention the channel by using #<channel name>):")
                leave_messages_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                leave_messages_channel_id = leave_messages_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['leave_messages'] = str(leave_messages_channel_id)

                # Daily guild points channel
                await ctx.send("Reference your daily guild points channel (Mention the channel by using #<channel name>):")
                daily_guild_points_channel_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                daily_guild_points_channel_id = daily_guild_points_channel_mention.channel_mentions[0].id
                config['text_channel_ids']['daily_guild_points'] = str(daily_guild_points_channel_id)



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

                # Bots role
                await ctx.send("Reference the bots role (Mention the role by using @<role name>):")
                bots_role_mention = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout = timeout_time_in_seconds)
                bots_role_id = bots_role_mention.role_mentions[0].id
                config['role_ids']['bots'] = str(bots_role_id)
                
                


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