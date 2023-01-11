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
    
    
class information(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #information command
    @commands.has_permissions(administrator = True)
    @commands.command(aliases=["i", "inform", "information"], brief="information",description="View server information")
    async def info(self, ctx, member: discord.Member=None):
        await ctx.channel.purge(limit = 1)
        embed1 = discord.Embed(
            color = embed_color
            )
        embed1.set_image(url = "https://imgur.com/iW22uIC.png")
        embed2 = discord.Embed(
            description = "Welcome to QTmoon'y Community discord server. Be sure to view all of our rules and select our self-roles. Please do not abuse any server bots and members. In order to use our bot please use **!help** to view the bot's commands menu.\n\n**🦾 | Bingus Bot**\nHelp Command ➜ `!help`\n\n**📌 | Usefull Channels**\nView new members ➜ <#1052126801150873654>\nAnnouncements ➜ <#1052134391758979082>\nServer Rules ➜ <#1052126800991494187>\nSelf Role Selection ➜ <#1052131759107625030>\n\n**📱 | QTmoony's Socials**\nTwitch Link ➜ https://twitch.tv/QTmoony \nTwitter ➜ https://twitter.com/QTmoony1 \nInstagram ➜ https://tinyurl.com/4nr76hxv \n\nfor any additional help or information please contact a <@&1052947612615049248>. Enjoy your stay!",
            color = embed_color
            )
        embed2.timestamp = datetime.datetime.now()
        embed2.set_footer(text="©️ Moonies QTees", icon_url=ctx.guild.icon.url)
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        
        
    @info.error
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
    await client.add_cog(information(client))