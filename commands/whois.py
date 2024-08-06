import discord
from discord.ext import commands
import json
import discord.ui

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    
    
class userinformation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
    #whois command
    @commands.has_permissions(administrator = True)
    @commands.hybrid_command(aliases=["who", "ui", "userinfo"], brief="who [@member name]",description="View a members information", with_app_command=True)
    async def whois(self, ctx, user:discord.Member=None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(
            title= f"**User Info of {user}**",
            colour = embed_color,
            timestamp = ctx.message.created_at
        )
        #embed.set_thumbnail(url = user.avatar.url)
        if(user.avatar):
            embed.set_thumbnail(url = "{}".format(user.avatar.url))
        if(ctx.author.avatar):
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url) #ctx.guild.icon.url for server icon
        else:
            embed.set_footer(text = f"Requested by {ctx.author}") #ctx.guild.icon.url for server icon
        embed.add_field(name = "ID:", value=user.id, inline=False)
        embed.add_field(name="Name:", value=user.display_name, inline=False)
        embed.add_field(name="Account Created on:", value=user.created_at, inline=False)
        embed.add_field(name="Joined Server On:", value=user.joined_at, inline=False)
        embed.add_field(name="Classifies as a bot:", value=user.bot, inline=False)
        await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(userinformation(client))