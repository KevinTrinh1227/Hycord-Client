import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    
class information(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #information command
    @commands.has_permissions(administrator = True)
    @commands.hybrid_command(aliases=["i", "inform", "info"], brief="information",description="View server information", with_app_command=True)
    async def information(self, ctx):
        await ctx.channel.purge(limit = 1)
        """
        embed1 = discord.Embed(
            color = embed_color
            )
        embed1.set_image(url = "https://imgur.com/iW22uIC.png")
        """
        embed2 = discord.Embed(
            description = """
            *THIS OUTPUT IS PLACEHOLDER
            TO CHANGE PLEASE GO TO "~/Hycord-Bot/commands/information.py"
            AND EDIT THE FILE*
            
            Welcome to the discord server discord server. Be sure to view all of our rules and select our self-roles. Please do not abuse any server bots and members. In order to use our bot please use **!help** to view the bot's commands menu.
            
            For any additional help or information please contact a staff member. Enjoy your stay!""",
            color = embed_color
            )
        embed2.timestamp = datetime.datetime.now()
        embed2.set_footer(text=f"©️ {ctx.guild.name}", icon_url=ctx.guild.icon.url)
        #await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        
        
async def setup(client):
    await client.add_cog(information(client))