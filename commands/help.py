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
embed_color = int(data["general"]["embed_color"].strip("#"), 16)  # convert hex color to hexadecimal format

class HelpView(discord.ui.View):
    def __init__(self, client, ctx, command_list, page):
        super().__init__(timeout=60)
        self.client = client
        self.ctx = ctx
        self.command_list = command_list
        self.page = page
        self.items_per_page = 5
        self.total_pages = math.ceil(len(command_list) / self.items_per_page)

    async def update_embed(self):
        start_index = (self.page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page

        embed = discord.Embed(
            title=f"📜** | Command Help (Page {self.page}/{self.total_pages})**",
            description="Note: some commands may require server permissions to run.",
            color=embed_color
        )

        for command in self.command_list[start_index:end_index]:
            aliases = " | ".join(command.aliases) if command.aliases else "No aliases"
            description = f"`{command.description}`" if command.description else "No description"
            usage = f"`{self.ctx.prefix}{command.brief}`" if command.brief else "No example usage"
            
            embed.add_field(
                name=f"{command.name} ({aliases})",
                value=f"Description: {description}\nUsage: {usage}",
                inline=False
            )

        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -= 1
        if self.page <= 1:
            button.disabled = True
        self.next_button.disabled = False
        embed = await self.update_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        if self.page >= self.total_pages:
            button.disabled = True
        self.previous_button.disabled = False
        embed = await self.update_embed()
        await interaction.response.edit_message(embed=embed, view=self)

class HelpCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def send_help(self, ctx: commands.Context, command_list, page):
        view = HelpView(self.client, ctx, command_list, page)
        embed = await view.update_embed()
        view.previous_button.disabled = page <= 1
        view.next_button.disabled = page >= view.total_pages
        await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(aliases=["h"], brief="help [page number]", description="View commands help menu", with_app_command=True)
    async def help(self, ctx: commands.Context, page: int = 1):
        command_list = [cmd for cmd in self.client.commands if not cmd.hidden]
        await self.send_help(ctx, command_list, page)

    @commands.Cog.listener()
    async def on_ready(self):
        print('HelpCog loaded.')

async def setup(client):
    await client.add_cog(HelpCog(client))
