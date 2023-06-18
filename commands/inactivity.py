import discord
from discord.ext import commands
import json
import requests
import datetime

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
inactivity_channel_id = int(data["text_channel_ids"]["inactivity_notice"]) #channel id from json file

class inactive(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    
    @commands.command(aliases = ["inactivity", "mia"], pass_context=True, brief="inactive", description="Let others know that you will be inactive")
    async def inactive(self, ctx):
        
        try:
            with open("verified_accounts.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open("verified_accounts.json", "w") as f:
                json.dump({}, f)
        
        try:
            user_id = str(ctx.author.id)
            if user_id in self.data:
                
                await ctx.send("How long will you be gone for?")
                inactive_duration = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
                
                await ctx.send("Please provide your reasoning on why you will be inactive.")
                inactive_reason = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
                
                uuid = self.data[user_id]["uuid"]
                playerdb_url = f'https://playerdb.co/api/player/minecraft/{uuid}'
                username_requests = requests.get(playerdb_url)
                user_data = username_requests.json()
                username = user_data["data"]["player"]["username"]
                
                #grabbing inactivity channel from json file
                channel = self.client.get_channel(inactivity_channel_id)
                
                embed = discord.Embed(
                    title = f"**Inactivity Notice from {ctx.author.name} ⌛**", 
                    colour = embed_color
                    )
                embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                embed.add_field(name='IGN', value=f"`{username}`", inline=True)
                embed.add_field(name='Discord Tag', value=f"`{ctx.author}`", inline=True)
                embed.add_field(name='Inactivity Duration', value=f"`{inactive_duration.content}`", inline=True)
                embed.add_field(name='Reasoning', value = f"{inactive_reason.content}")
                embed.set_thumbnail(url = f"https://visage.surgeplay.com/head/192/{uuid}?y=15")
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                
                await ctx.send(f"Your inactivity notice has been listed on {channel.mention}.")
                await channel.send(embed=embed)
                
            else:
                await ctx.send("Your Discord account is not linked to a Minecraft account.")
                
        except:
            await ctx.send("ERROR. Please message a staff member.")
        
        
async def setup(client):
    await client.add_cog(inactive(client))
    

