import discord
from discord.ext import commands
import json

class MinecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def linktest(self, ctx, minecraft_username: str):
        """Links your Discord account to a Minecraft account."""
        # Save the data in a JSON file
        data = {}
        data['minecraft_username'] = minecraft_username
        data['discord_id'] = ctx.author.id
        with open('minecraft_data.json', 'w') as f:
            json.dump(data, f)

        await ctx.send(f'Successfully linked Minecraft account {minecraft_username} to Discord ID {ctx.author.id}')
        
async def setup(client):
    await client.add_cog(MinecraftCog(client))