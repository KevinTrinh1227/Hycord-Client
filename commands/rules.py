import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    
    
class rules(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #server rules cmd
    @commands.has_permissions(administrator = True)
    @commands.command(aliases=["rule", "regulations", "r"], brief="rules",description="View server rules")
    async def rules(self, ctx, member: discord.Member=None):
        embed = discord.Embed(
            title = "**DISCORD SERVER RULES**",
            description = "Pitch Black is dedicated to making the server an enjoyable/safe experience for everyone, regardless of gender, sexuality, race, etc. All broken rules will be met with a punishment based on severity of the situation.\n\n**Follow these 5 rules, and your chillin.**\n \n**Rule #1** ➜ Do not Catfish. \n \n**Rule #2** ➜ Do not be an asshole.\n \n**Rule #3** ➜ Do not do immature things. \n \n**Rule #4** ➜ Do not abuse anything.\n \n**Rule #5** ➜ And all of the above. \n \nReport all rule breakers to a <@&1054983260473671742>. And be sure to disable direct messages with shared server members.\n",
            color = embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_image(url="https://i.gyazo.com/a7413858cfdbf1d44906326f512a19e2.gif")
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url=ctx.guild.icon.url)
        await ctx.channel.purge(limit = 1)
        await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(rules(client))