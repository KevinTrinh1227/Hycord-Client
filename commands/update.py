import discord
from discord.ext import commands
import requests
import discord.ui
import datetime
import json
import os
from dotenv import load_dotenv


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    

class update_account(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}
            
    #bedwars stats command
    @commands.command(aliases=["relink", "resync"], brief="Updates your discord information",description="update your account profile on discord")
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
            url = f"https://playerdb.co/api/player/minecraft/{uuid}"
            try: 
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    username = data['data']['player']['username'] # gets updated username
            except Exception as e:
                error_message = f"An unexpected error occurred: {e}"
                await ctx.send(error_message)

            hypixel_api_key = os.getenv("HYPIXEL_API_KEY")

            requestlink = f"https://api.hypixel.net/player?key={hypixel_api_key}&uuid={uuid}"
            hydata = requests.get(requestlink).json()

            #other bedwars stats
            bedwars_level = hydata["player"]["achievements"]["bedwars_level"] #bedwars level
            new_nickname = f"[{bedwars_level}✫] {username}"

            embed = discord.Embed(
                title = f"**Successfully Updated Account** ✅",
                url = f"https://plancke.io/hypixel/player/stats/{username}",
                description = f"You have **successfully** updated your profile.",
                color = embed_color               
            )
            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.add_field(name='IGN', value=username, inline=True)
            embed.add_field(name='Level', value=f"{bedwars_level}✫", inline=True)
            embed.add_field(name='UUID', value=uuid, inline=True)
            embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/128/{uuid}")
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)

            await ctx.author.edit(nick=new_nickname)
            await ctx.send(f"{ctx.author.mention}'s account is has just been updated.", embed=embed)

            
        else:
            embed = discord.Embed(
                title = f"**You cant update your account!** ❌",
                description = f"{ctx.author} was not found in the verified accounts list. Please link your account first before trying this command.",
                color = embed_color
            )
            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(update_account(client))        