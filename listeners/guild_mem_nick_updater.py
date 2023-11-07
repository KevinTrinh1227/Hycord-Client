import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

guild_id = int(data["general"]["discord_server_guild_id"])
verification_template = data["embed_templates"]["verification_nickname"]
enable_feature = bool(data["features"]["auto_daily_gexp"])
embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
logs_channel_id = int(data["text_channel_ids"]["bot_logs"])    # logs the bot logs in this channel


already_sent = False

class guild_discord_nick_updater(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.guild_discord_nick_updater.start()
        
    @tasks.loop(seconds=300)  # Run every 300 seconds / 5 minutes
    async def guild_discord_nick_updater(self):
        
        guild = self.client.get_guild(guild_id)
        
        # Load data from 'verified_accounts.json' and 'guild_cache.json'
        with open('verified_accounts.json', 'r') as verified_accounts_file:
            verified_accounts_data = json.load(verified_accounts_file)

        with open('guild_cache.json', 'r') as guild_cache_file:
            guild_cache_data = json.load(guild_cache_file)

        # Extract members from 'guild_cache.json'
        members = guild_cache_data['guild_data']["guild"]['members']

        # Iterate through the members and check for matches in 'verified_accounts.json'
        for member in members:
            member_uuid = member['uuid']
            for discord_id, info in verified_accounts_data.items():
                if member_uuid == info['uuid']:
                    username = info['username']
                    rank = member['rank']
                    
                    member = guild.get_member(int(discord_id))
                    
                    guild_nickname = verification_template["verified_guild_member"].format(
                        ign = username,
                        guild_rank = rank
                    )

                    #print(member.display_name)
                    try:
                        if guild_nickname != member.display_name:
                            # print(f"Current: {member.display_name} did NOT match required: {guild_nickname}. Now renaming to: {guild_nickname}")
                            
                            channel = self.client.get_channel(logs_channel_id)
                            embed = discord.Embed(
                                title=(f"👤 | Updated guild member's discord nickname."),
                                description=f"{member.mention}'s server nickname has been updated. Name Change: `{member.display_name}` ➜ `{guild_nickname}`.",
                                colour= embed_color
                            )
                            # embed.timestamp = datetime.datetime.now()
                            embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/{member_uuid}.png?y=-40")
                            # embed.set_footer(text=f"©️ {guild.name}", icon_url = guild.icon.url)
                            try:
                                await member.edit(nick=guild_nickname)
                                await channel.send(embed=embed)
                            except: # this means that the bot could not rename a specific person that has higher priorities.
                                pass

                        else:
                            # print("Nick name already matched so skipping...")
                            # print(f"Discord Nick: {member.display_name}, Member UUID: {member_uuid}, Username: {username}, Rank: {rank}")
                            pass
                    except:
                        pass
        
        
async def setup(client):
    await client.add_cog(guild_discord_nick_updater(client))