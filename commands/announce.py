import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = data["embed_color"]
embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

class announce(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #accouncement/say command   
    @commands.has_permissions(administrator = True)
    @commands.command(aliases = ["announce", "announcement", "a"], brief="say [Your Message]",description="Make an anouncement embed message.")
    async def say(self, ctx, *, message):
        embed = discord.Embed(
            title = "**Server Announcement**",
            description = message,
            color = embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="©️ Moonies QTees", icon_url = ctx.guild.icon.url)
        await ctx.channel.purge(limit = 1)
        await ctx.send(embed = embed)
        
        
    @say.error
    async def ban_error(self, ctx, error):
        #if user does not have the permission node
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_image(url="https://imgur.com/nU9QbXv.png")
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        #if the command was missing arguments
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_image(url="https://imgur.com/tQzEKFv.png")
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        #other error
        else:
            print(error) # for other errors so they dont get suppressed
        
        
async def setup(client):
    await client.add_cog(announce(client))