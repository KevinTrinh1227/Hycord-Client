import discord
from discord.ext import commands
import json

class MinecraftDisplayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def displaytest(self, ctx):
        """Displays your linked Minecraft username."""
        # Load the data from the JSON file
        with open('minecraft_data.json', 'r') as f:
            data = json.load(f)

        # Check if the user has a linked Minecraft account
        if str(ctx.author.id) in data:
            await ctx.send(f'Your linked Minecraft username is {data[str(ctx.author.id)]["minecraft_username"]}')
        else:
            await ctx.send('You have not linked a Minecraft account to your Discord account.')
            
async def setup(client):
    await client.add_cog(MinecraftDisplayCog(client))