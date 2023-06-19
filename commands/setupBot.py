import discord
from discord.ext import commands
import json
import requests
import datetime

class SetupCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["botsetup"], pass_context=True, brief="setup", description="Setup the bot configurations")
    async def setup(self, ctx):
        # Read the existing config.json file
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        try:
            # General bot prefix
            await ctx.send("Enter a bot command prefix (e.g., `!` or `.`):")
            chosen_command_prefix = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
            config['general']['bot_prefix'] = chosen_command_prefix.content

            # General embed color
            await ctx.send("Please enter the embed color (in hex format, e.g., #ff0000 for red):")
            chosen_hex_color = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
            config['general']['embed_color'] = chosen_hex_color.content

            # General discord guild ID
            guild_id = ctx.guild.id
            config["general"]["discord_server_guild_id"] = str(guild_id)


    
            # Filtered chat
            await ctx.send("Enable filtered chat? (0 for No, 1 for Yes):")
            filtered_chat = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
            config['features']['filtered_chat'] = int(filtered_chat.content)

            # Auto GEXP
            await ctx.send("Enable automatic GEXP daily messages? (0 for No, 1 for Yes):")
            auto_gexp = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
            config['features']['auto_gexp'] = int(auto_gexp.content)

            # Inactivity command
            await ctx.send("Enable inactivity command? (0 for No, 1 for Yes):")
            inactivity_cmd = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
            config['features']['inactivity_cmd'] = int(inactivity_cmd.content)

            # Punishments command
            await ctx.send("Enable punishments command? (0 for No, 1 for Yes):")
            punishments_cmd = await self.client.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
            config['features']['punishments_cmd'] = int(punishments_cmd.content)


            # Save the updated config to config.json
            with open('config.json', 'w') as config_file:
                json.dump(config, config_file, indent=2)

            await ctx.send("Configuration updated successfully.")
        except:
            await ctx.send("No response received. Please try again.")


async def setup(client):
    await client.add_cog(SetupCog(client))
