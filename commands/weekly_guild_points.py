import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import requests
import discord.ui
import datetime
import time
import json
import os
from dotenv import load_dotenv
import time

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
hypixel_guild_id = data["hypixel_ids"]["guild_id"]


class guildPoints(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    async def get_player_stats(self, username):
        hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
        # Get the UUID from Mojang API
        uuid_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        uuid_response = requests.get(uuid_url)
        if uuid_response.status_code != 200:
            return None, None  # Return None if the player doesn't exist
        uuid = uuid_response.json()['id']

        # Get the guild data from Hypixel API
        guild_url = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
        guild_response = requests.get(guild_url)
        if guild_response.status_code != 200:
            return None, None  # Return None if the guild doesn't exist
        guild_data = guild_response.json()

        # Search for the player's data in the guild members
        for member in guild_data["guild"]["members"]:
            if member["uuid"] == uuid:
                return uuid, member

        return None, None  # Return None if the player is not in the guild
    
    @commands.hybrid_command(aliases = ["wgp", "weeklygp"], brief="guildpoints [Guild Member IGN]", description="Shows a specified guild member's weekly points", with_app_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user) # 1 use for every 10 seconds.
    async def weeklypoints(self, ctx, *, username):
        uuid, member_data = await self.get_player_stats(username)

        # this if statement is if the member is not found inside the guild
        if uuid is None:
            embed = discord.Embed(
            title=f"{username} was not found!",
            description=f"{username} is either not in your guild, or does not exist. Please try again or contact a staff member if this is a mistake.",
            color=embed_color  # You can customize the color
            )
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/{username}.png?y=-40"),
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)

            await ctx.send(embed=embed)
            return
        
        member_skin_image = f"https://visage.surgeplay.com/bust/{uuid}.png?y=-40"

        guild_data = member_data["expHistory"]
        guild_points = [(date, points) for date, points in guild_data.items()]
        
        current_time = int(time.time() * 1000)  # Get the current time in milliseconds
        member_age_ms = current_time - member_data["joined"]
        member_age_days = member_age_ms / (1000 * 60 * 60 * 24)
        

        # Calculate the average points
        points_list = [points for _, points in guild_points]
        average_points = sum(points_list) / len(points_list)
        
        weekly_points = "\n".join([f"- {date}: {points}" for date, points in guild_points])

        embed = discord.Embed(
            title=f"{username}\'s Weekly Report",
            description=f"""
            `{uuid}`
            
            **Weekly average:** {average_points:.2f} GP
            
            {weekly_points}
            """,
            color=embed_color  # You can customize the color
        )
        embed.set_thumbnail(url=member_skin_image),
        embed.add_field(name="Guild Rank", value=member_data["rank"])
        try:
            embed.add_field(name="Quests", value=member_data["questParticipation"])
        except:
            embed.add_field(name="Quests", value="None")
        embed.add_field(name="Time In Guild", value=f"{member_age_days:.2f} days")

        await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(guildPoints(client))
    

