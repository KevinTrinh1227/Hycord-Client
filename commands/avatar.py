import discord
from discord.ext import commands
import json
import discord.ui

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    
    
class useravatar(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    
    #avatar cmd
    @commands.command(aliases=["av", "pfp"], brief="av [@member name]",description="Get a users avatar image.")
    async def avatar(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title = f"{member.name}'s avatar",
            color = embed_color
        )
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.set_image(url = "{}".format(member.avatar.url))
        await ctx.send(embed=embed)
        

async def setup(client):
    await client.add_cog(useravatar(client))