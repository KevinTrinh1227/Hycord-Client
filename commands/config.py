import discord
from discord.ext import commands
import json

class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(
        aliases=["sendconfig"], 
        brief="config", 
        description="Sends out the bot config file", 
        with_app_command=True
    )
    async def config(self, ctx):
        """
        Sends the config.json file contents.
        Usage:
        - Send as file: !config
        """
        file_path = 'config.json'
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                json_content = json.loads(content)
                pretty_content = json.dumps(json_content, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            await ctx.send(f"Error reading file: {str(e)}")
            return
        
        if len(pretty_content) > 2000:
            # await ctx.send("The content is too large to send as text, sending as file instead.")
            await ctx.send(file=discord.File(file_path))
        else:
            await ctx.send(f"```json\n{pretty_content}\n```")

async def setup(client):
    await client.add_cog(Config(client))
