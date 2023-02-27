import discord.ui
import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = data["embed_color"]
embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
verified_role_id = int(data["verified_role_id"]) #verified role id
guild_member_role_id = int(data["guild_member_role_id"]) #guild role

class verifiedstats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["vs", "vstats"], brief="verifiedstats",description="Shows stats of verified accounts")
    async def verifiedstats(self, ctx):
        with open('verified_accounts.json', 'r') as f:
            data = json.load(f)
        num_linked = len(data)

        role_id_1 = verified_role_id #verified role id
        role_id_2 = guild_member_role_id #guild role

        role_1 = discord.utils.get(ctx.guild.roles, id=role_id_1)
        role_2 = discord.utils.get(ctx.guild.roles, id=role_id_2)
        total_guild_members = len(role_2.members)

        num_with_both_roles = len(set(role_1.members).intersection(set(role_2.members))) #checks 

        num_bots = sum(1 for member in ctx.guild.members if member.bot) #gets the number of bots
        num_users = len(ctx.guild.members) #total members in server

        not_linked = num_users - (num_bots + num_linked)

        embed = discord.Embed(
            title="Verified Accounts",
            description = f"Now showing your server's verified users statistics.",
            colour = embed_color
            )
        embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url),
        embed.add_field(name='Not Verified', value=f"{not_linked} users", inline=True),
        embed.add_field(name='Guild Members', value=f"{num_with_both_roles}/{total_guild_members} verified", inline=True),
        embed.add_field(name='Total Verifies', value=f"{num_linked} users", inline=True),
        embed.set_thumbnail(url = "{}".format(ctx.guild.icon.url)),
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url=ctx.guild.icon.url)
        embed.timestamp = datetime.datetime.now()

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(verifiedstats(client))