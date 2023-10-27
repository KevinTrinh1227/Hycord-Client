import discord
from discord.ext import commands
import requests
import discord.ui
import datetime
import json
import os
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv
import utils.guild_data as guild


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    

class update_account(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}
            
    #bedwars stats command
    @commands.hybrid_command(aliases=["relink", "resync"], brief="Updates your discord information", description="update your account profile on discord", with_app_command=True)
    @commands.cooldown(1, 3600, commands.BucketType.user) # 1 use for every 10 minutes cooldown.
    async def update(self, ctx):
        
        member = ctx.message.author
        try:
            with open("verified_accounts.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open("verified_accounts.json", "w") as f:
                json.dump({}, f)

        if str(member.id) in self.data:

            #load in .env variables
            load_dotenv() 

            uuid = self.data[str(member.id)]["uuid"]
            username_url = f'https://api.mojang.com/user/profile/{uuid}'
            ign_response = requests.get(username_url)
            if ign_response.status_code == 200:
                ign = ign_response.json()['name']
            else:
                ign = "Username Not Found"  # if API fails
                
            # Load the JSON data from the "guild_cache.json" file
            with open("guild_cache.json", "r") as json_file:
                guild_cache = json.load(json_file)

            # Check if the target UUID exists in the JSON data
            if uuid in guild_cache:
                before_name = guild.search_uuid_and_return_name("guild_cache.json", uuid)
                if before_name != ign:
                    guild.update_username("guild_cache.json", uuid, ign)

            embed = discord.Embed(
                title = f"**✅ | Successfully Updated Account**",
                url = f"https://plancke.io/hypixel/player/stats/{ign}",
                description = f"You have **successfully** updated your profile.",
                color = embed_color               
            )
            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.add_field(name='IGN', value=ign, inline=True)
            embed.add_field(name='UUID', value=uuid, inline=True)
            embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/{uuid}.png?y=-40")
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)

            await ctx.author.edit(nick=ign)
            await ctx.send(f"{ctx.author.mention}'s account is has just been updated.", embed=embed)

            
        else:
            embed = discord.Embed(
                title = f"**❌ | You cant update your account!**",
                description = f"{ctx.author} was not found in the verified accounts list. Please link your account first before trying this command.",
                color = embed_color
            )
            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(update_account(client))     