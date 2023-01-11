import discord
from discord.ext import commands
import json
import asyncio

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = data["embed_color"]
embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
    @commands.command(aliases = ["lt", "pong"], pass_context=True, brief="ping",description="View bot latency connection")
    async def ping(self, ctx):
        await ctx.channel.purge(limit = 1)
        ping1 = round(self.client.latency * 1000)
        async with ctx.typing():
            await asyncio.sleep(0.1)
        ping2 = round(self.client.latency * 1000)
        async with ctx.typing():
            await asyncio.sleep(0.25)
        ping3 = round(self.client.latency * 1000)
        async with ctx.typing():
            await asyncio.sleep(0.50)
        ping4 = round(self.client.latency * 1000)
        async with ctx.typing():
            await asyncio.sleep(0.75)
        ping5 = round(self.client.latency * 1000)
        async with ctx.typing():
            await asyncio.sleep(1)
        ping6 = round(self.client.latency * 1000)
        sum_of_pings = sum([ping1, ping2, ping3, ping4, ping5, ping6])
        avg_ping = sum_of_pings / 6
        embed = discord.Embed(
            title="Connection Latency Tests", 
            description = f"After 6 latency ping checks have been made, the bot's average ping is: **{avg_ping}ms**. Each of the ping tests are posted below.",
            colour = embed_color
            )
        embed.add_field(name='Ping Test #1', value=f"{str(ping1)}ms", inline=True)
        embed.add_field(name='Ping Test #2', value=f"{str(ping2)}ms", inline=True)
        embed.add_field(name='Ping Test #3', value=f"{str(ping3)}ms", inline=True)
        embed.add_field(name='Ping Test #4', value=f"{str(ping4)}ms", inline=True)
        embed.add_field(name='Ping Test #5', value=f"{str(ping5)}ms", inline=True)
        embed.add_field(name='Ping Test #6', value=f"{str(ping6)}ms", inline=True)
        embed.set_thumbnail(url = "{}".format(ctx.guild.icon.url))
        embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(ping(client))
    

