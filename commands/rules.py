import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    
# Load the "server_rules" template
server_rules_template = data["embed_templates"]["server_rules"]


embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    
class rules(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #server rules cmd
    @commands.has_permissions(administrator = True)
    @commands.hybrid_command(aliases=["rule", "regulations", "r"], brief="rules",description="View server rules", with_app_command=True)
    async def rules(self, ctx):
        
        # Replace the footer text with actual values
        footer_text = server_rules_template["footer_text"].format(
            guild_name=ctx.guild.name
        )

        embed = discord.Embed(
            title=server_rules_template["title"],
            description=server_rules_template["description"],
            color=embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=footer_text, icon_url=ctx.guild.icon.url)
        # await ctx.channel.purge(limit = 1)
        await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(rules(client))