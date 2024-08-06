import discord
from discord.ext import commands
import json
import discord.ui
import os
import sys

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

class Restart(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(aliases=["restartclient", "restartbot", "reload"], brief="restart", description="Restart the client", with_app_command=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def restart(self, ctx):
        try:
            await ctx.send("Client is now restarting, please wait about 10 seconds...")
            # Use absolute path for executable and script
            executable = sys.executable
            script = os.path.abspath(sys.argv[0])
            os.execv(executable, [executable, script])
        except Exception as e:
            await ctx.send(f"An error occurred while trying to restart the client: {e}. Please check terminal.")

async def setup(client):
    await client.add_cog(Restart(client))
