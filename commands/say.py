import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16)  # convert hex color to hexadecimal format


class say(commands.Cog):
    def __init__(self, client):
        self.client = client

    # say command
    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(aliases=["s", "yell"], brief="say [Your Message]", description="Say message as an embed", with_app_command=True)
    async def say(self, ctx, *, message):
        embed = discord.Embed(
            title=f"**{ctx.guild.name} | Announcement**",
            description=message,
            color=embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"© {ctx.guild.name}", icon_url=ctx.guild.icon.url)
        #await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(say(client))