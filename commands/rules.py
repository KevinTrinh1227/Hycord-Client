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
    @commands.hybrid_command(aliases=["rule", "regulations", "r"], brief="rules",description="View server rules", with_app_command=True)
    async def rules(self, ctx):
        embed = discord.Embed(
            title = "**DISCORD SERVER RULES**",
            description = """

            *THIS IS A PLACE HOLDER RULES COMMAND*
            *TO MAKE ANY EDITS GO TO "~/Hycord-Bot/commands/rules.py"*

            (+) Be respectful and kind to all members.
            (+) No spamming or excessive advertising.
            (+) Use appropriate and safe-for-work content.
            (+) No discrimination or offensive language.
            (+) Respect privacy and don't share personal information without consent.
            (+) Stay on-topic and avoid derailing discussions.
            (+) Follow Discord's terms of service and guidelines.
            (+) No trolling, baiting, or disruptive behavior.
            (+) Respect server staff and their instructions.
            (+) Report issues to server staff.
            (+) No excessive self-promotion or spamming personal links.
            (+) Keep discussions civil and avoid arguments.
            """,
            color = embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url=ctx.guild.icon.url)
        await ctx.channel.purge(limit = 1)
        await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(rules(client))