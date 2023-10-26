import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    
# Load the "server_rules" template
server_information_template = data["embed_templates"]["information"]

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    
class information(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #information command
    @commands.has_permissions(administrator = True)
    @commands.hybrid_command(aliases=["i", "inform", "info"], brief="information",description="View server information", with_app_command=True)
    async def information(self, ctx):
        
        # Replace the footer text with actual values
        footer_text = server_information_template["footer_text"].format(
            guild_name=ctx.guild.name
        )
        
        embed2 = discord.Embed(
            title=server_information_template["title"],
            description = server_information_template["description"],
            color = embed_color
            )
        embed2.timestamp = datetime.datetime.now()
        embed2.set_footer(text=footer_text, icon_url=ctx.guild.icon.url)
        await ctx.send(embed=embed2)
        
        
async def setup(client):
    await client.add_cog(information(client))