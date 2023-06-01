import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime
import discord.ui
import json


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format


class purge(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #chat purge command (and command removal)   
    @commands.has_permissions(manage_messages = True)
    @commands.command(aliases = ["del", "delete", "clear"], brief="purge [integer value]",description="Clear a specified amount of chat messages")
    async def purge(self, ctx, amount : int):
        await ctx.channel.purge(limit = amount + 1)


async def setup(client):
    await client.add_cog(purge(client))