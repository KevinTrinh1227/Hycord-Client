import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    
#json data to run bot
bot_prefix = data["bot_prefix"]
embed_color = data["embed_color"]
embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format


class commend_error(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title=(f"Help Command: `{bot_prefix}help`"),
                colour= embed_color
                )
            embed.timestamp = datetime.datetime.now()
            embed.set_image(url="https://imgur.com/8JjulFq.png")
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            print(error) #prints to console
    
        
async def setup(client):
    await client.add_cog(commend_error(client))
    
    

