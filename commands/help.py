import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime
import discord.ui
import json
import asyncio
from discord.utils import get
import math
from discord.ext.commands import Paginator

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

bot_prefix = data["general"]["bot_prefix"]
embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_help(self, ctx, command_list, page):
        items_per_page = 5
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        if start_index >= len(command_list):
            await ctx.send("No more pages.")
            return

        embed = discord.Embed(
            title=f"📜** | Command Help (Page {page})**",
            description="Note: some commands may require server permissions to run.",
            color=embed_color
        )

        for command in command_list[start_index:end_index]:
            aliases = " | ".join(command.aliases) if command.aliases else "No aliases"
            description = f"`{command.description}`" if command.description else "No description"
            usage = f"`{ctx.prefix}{command.brief}`" if command.brief else "No example usage"
            
            embed.add_field(
                name=f"{command.name} ({aliases})",
                value=f"Description: {description}\nUsage: {usage}",
                inline=False
            )

        message = await ctx.send(embed=embed)

        # Add reaction emojis
        if page > 1:
            await message.add_reaction("⬅️")
        if end_index < len(command_list):
            await message.add_reaction("➡️")

        # Reaction check function
        def check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == message.id
                and str(reaction.emoji) in ["⬅️", "➡️"]
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
                await message.remove_reaction(reaction, user)
                if str(reaction.emoji) == "⬅️":
                    page -= 1
                elif str(reaction.emoji) == "➡️":
                    page += 1
                await ctx.channel.purge(limit = 1)      # deletes the previous page
                await self.send_help(ctx, command_list, page)   # sends the new page number
            except asyncio.TimeoutError:
                break

    @commands.command(aliases=["h"], brief="help [page number]",description="View commands help menu")
    async def help(self, ctx, page: int = 1):
        # Filter out commands that are hidden
        command_list = [cmd for cmd in self.bot.commands if not cmd.hidden]

        await self.send_help(ctx, command_list, page)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'HelpCog loaded.')


async def setup(client):
    await client.add_cog(HelpCog(client))
    

