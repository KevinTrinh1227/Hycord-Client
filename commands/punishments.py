import discord
from discord.ext import commands
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

command_prefix = data["general"]["bot_prefix"]
embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

#private staff channel ID number
#this is where the priv_embed will be displayed.
priv_staff_channel = int(data["text_channel_ids"]["bot_logs"])


class punishments(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.has_permissions(kick_members=True)
    @commands.hybrid_command(aliases=["k"], brief="kick [member]", description="Kick a member from the server", with_app_command=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        if reason == None:
            reason = "No reason was provided."
        
        #public embed message for original ctx channel
        embed = discord.Embed(
            title=f"{member.display_name} has been kicked", 
            description=f"**User Tag:** {member.mention}\n\n**Reason:** {reason}",
            colour=embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url=f"{member.avatar.url}")
        embed.set_footer(text=f"©️ {member.guild.name}", icon_url=ctx.guild.icon.url)
        
        #embed to be displayed in the punishments priv channel
        priv_embed = discord.Embed( 
            title=f"{member.display_name} has been kicked", 
            description=f"**User Tag:** {member.mention}\n\n**Kicked By:** {ctx.author.mention}\n\n**Reason:** {reason}",
            colour=embed_color
        )
        priv_embed.timestamp = datetime.datetime.now()
        priv_embed.set_thumbnail(url=f"{member.avatar.url}")
        priv_embed.set_footer(text=f"Kicked by {ctx.author}", icon_url=ctx.author.avatar.url)
        
        await ctx.guild.kick(member)
        await self.client.get_channel(priv_staff_channel).send(embed=priv_embed)
        await ctx.send(embed=embed)

        
    @commands.has_permissions(ban_members=True)
    @commands.hybrid_command(aliases=["b"], brief="ban [member]", description="Perm ban a server member", with_app_command=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        if reason == None:
            reason = "No reason was provided."
    
        #embed to be displayed in the original context channel
        embed = discord.Embed(     
            title=f"{member.display_name} has been banned", 
            description=f"**User Tag:** {member.mention}\n\n**Banned By:** {ctx.author.mention}\n\n**Reason:** {reason}",
            colour=embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url=f"{member.avatar.url}")
        embed.set_footer(text=f"©️ {member.guild.name}", icon_url=ctx.guild.icon.url)
        
        #embed to be displayed in the punishments priv channel
        priv_embed = discord.Embed( 
            title=f"{member.display_name} has been banned", 
            description=f"**User Tag:** {member.mention}\n\n**Reason:** {reason}",
            colour=embed_color
        )
        priv_embed.timestamp = datetime.datetime.now()
        priv_embed.set_thumbnail(url=f"{member.avatar.url}")
        priv_embed.set_footer(text=f"Banned by {ctx.author}", icon_url=ctx.author.avatar.url)
        
        await ctx.guild.ban(member)
        await self.client.get_channel(priv_staff_channel).send(embed=priv_embed)
        await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(punishments(client))