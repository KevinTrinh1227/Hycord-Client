import discord
from discord.ext import commands
import json
from datetime import datetime


# Open the JSON file and read in the data
with open('config.json') as json_file:
  data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
weekly_gexp_requirement = 10000

class lastjoined(commands.Cog):
  def __init__(self, client):
    self.client = client
     
  @commands.hybrid_command(aliases = ["gminpoints", "gmp"], brief="guildminimumpoints",description="Displays a list of all guild members that did not meet the weekly GEXP requirement.", with_app_command=True)
  async def guildminimumpoints(self, ctx: commands.Context):
    
    # Function to paginate the list of users
    def paginate_users(users_list, page_size):
        for i in range(0, len(users_list), page_size):
            yield users_list[i:i + page_size]
      
    with open('guild_cache.json', 'r') as guild_cache_file:
      guild_cache_data = json.load(guild_cache_file)

    # Find users with points less than the weekly requirement
    low_points_users = []
    total_guild_members = 0
    for member in guild_cache_data["guild_data"]["guild"]["members"]:
        total_guild_members += 1
        weekly_points = sum(member["expHistory"].values())
        if weekly_points < weekly_gexp_requirement:
            uuid = member["uuid"]
            username = guild_cache_data["usernames"].get(uuid)  # Fix here
            if username:
                low_points_users.append((username, weekly_points, uuid))

    # Sort the list by weekly points in ascending order
    low_points_users.sort(key=lambda x: x[1], reverse=True)


    # Format the list of users with index, username, and weekly points
    formatted_users_pages = paginate_users(low_points_users, 25)
    first_page = next(formatted_users_pages, None)
    
    percentage_members = (len(low_points_users) / total_guild_members) * 100

    if first_page:
        total_pages = (len(low_points_users) - 1) // 25 + 1

        formatted_users = "\n".join(
            [f"**{i + 1}.** [{username}](https://plancke.io/hypixel/player/stats/{uuid}) - `{points} GEXP`"
            for i, (username, points, uuid) in enumerate(first_page)])

        # Create the first embed
        embed = discord.Embed(
            title=f"⏰ | Members Below Weekly Req. [1/{total_pages}]",
            description=f"A total of `{len(low_points_users)}`/`{total_guild_members}` guild members did not meet the\n weekly GEXP requirement of `{weekly_gexp_requirement}` points.\n\n{formatted_users}\n\n**{percentage_members:.2f}%** of the guild is not meeting the requirement.",
            color=embed_color
        )
        # embed.set_thumbnail(url=ctx.guild.icon.url)  # Add this line if needed
        await ctx.send(embed=embed)

        # Create additional embeds for subsequent pages
        for page_num, page in enumerate(formatted_users_pages, start=2):
            formatted_users = "\n".join(
                [f"**{i + 1 + (page_num - 1) * 25}.** [{username}](https://plancke.io/hypixel/player/stats/{uuid}) - `{points} GEXP`"
                for i, (username, points, uuid) in enumerate(page)])

            embed = discord.Embed(
                title=f"⏰ | Members Below Weekly Req. [{page_num}/{total_pages}]",
                description=f"A total of `{len(low_points_users)}`/`{total_guild_members}` guild members did not meet the\n weekly GEXP requirement of `{weekly_gexp_requirement}` points.\n\n{formatted_users}\n\n**{percentage_members:.2f}%** of the guild is not meeting the requirement.",
                color=embed_color
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send("No users found.")
        
        
async def setup(client):
    await client.add_cog(lastjoined(client))