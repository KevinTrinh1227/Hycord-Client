import discord
from discord.ext import commands
import json
import requests

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = data["embed_color"]
embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

class inactive(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
    @commands.command(aliases = ["inactivity", "mia"], pass_context=True, brief="ping",description="View bot latency connection")
    async def inactive(self, ctx):
        
        await ctx.send("How long will you be gone for?")
        inactive_duration = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
        
        await ctx.send("Please provide your reasoning on why you will be inactive.")
        inactive_reason = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
        
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}?"
        response = requests.get(url)
        uuid = response.json()['id']
        
        
        embed = discord.Embed(
            title = f"Inactivity Notice from {ctx.author.name}", 
            colour = embed_color
            )
        embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.add_field(name='IGN', value=f"some ign", inline=True)
        embed.add_field(name='Discord Tag', value=f"{ctx.author}", inline=True)
        embed.add_field(name='Inactivity Duration', value=inactive_duration.content, inline=True)
        embed.add_field(name='Reasoning', value = inactive_reason.content, inline=True)
        embed.set_thumbnail(url = f"https://visage.surgeplay.com/head/192/{uuid}?y=15")
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
        await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(inactive(client))
    

