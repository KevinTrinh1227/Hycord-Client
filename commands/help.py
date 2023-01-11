import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime
import discord.ui
import json


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

bot_prefix = data["bot_prefix"]
embed_color = data["embed_color"]
embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format


class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Help command  
    @commands.command(aliases = ["h", "aid", "idk"], brief="help",description="View command help menu")
    async def help(self, ctx):
        
        commands = [c for c in self.client.commands]
        embed_description = ""
        for command in commands:
            embed_description += f"**{command.name[0].upper() + command.name[1:]}:** {command.description}\nCommand Aliases: `{', '.join(command.aliases)}`\nCommand Usage: `{bot_prefix}{command.brief}`\n\n"
        
        embed = discord.Embed(
            title = "General Commands",
            description = embed_description,
            color = embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
    
        
async def setup(client):
    await client.add_cog(help(client))
    

