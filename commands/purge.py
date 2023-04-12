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
        
    @purge.error
    async def kick_error(self, ctx, error):
        #if user does not have the permission node
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = f"**You are lacking permissions** ",
                description = f"You do not have the necessary permissions to run this command, please contact a staff member if you believe this is incorrect.",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
            await ctx.send(embed=embed)
        #if the command was missing arguments
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color = embed_color
            )
            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
            await ctx.send(embed=embed)
        #other error
        else:
            print(error) # for other errors so they dont get suppressed
        
async def setup(client):
    await client.add_cog(purge(client))