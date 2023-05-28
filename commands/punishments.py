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
priv_staff_channel = int(data["text_channel_ids"]["staff_chat"])


class punishments(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.has_permissions(kick_members=True)
    @commands.command(aliases = ["k"], brief="kick [@member name]",description="Kick a member from the server")
    async def kick(self, ctx, member:discord.Member, *, reason=None):
        if reason == None:
            reason = "No reason was provided."
        #public embed message for original ctx channel
        embed = discord.Embed(
            title=f"{member.display_name} has been kicked", 
            description = f"**User Tag:** {member.mention}\n\n**Reason:** {reason}",
            colour = embed_color
            )
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url = "{}".format(member.avatar.url))
        embed.set_footer(text=f"©️ {member.guild.name}", icon_url = ctx.guild.icon.url)
        embed.set_image(url="https://imgur.com/7l8D0pZ.png")
        
        #embed to be displayed in the pushments priv channel
        priv_embed = discord.Embed( 
            title=f"{member.display_name} has been kicked", 
            description = f"**User Tag:** {member.mention}\n\n**Kicked By:** {ctx.author.mention}\n\n**Reason:** {reason}",
            colour = embed_color
            )
        priv_embed.timestamp = datetime.datetime.now()
        priv_embed.set_thumbnail(url = "{}".format(member.avatar.url))
        priv_embed.set_footer(text = f"Kicked by {ctx.author}", icon_url=ctx.author.avatar.url)
        
        await ctx.guild.kick(member)
        await self.client.get_channel(priv_staff_channel).send(embed=priv_embed)
        await ctx.send(embed=embed)

        
    @kick.error
    async def kick_error(self, ctx, error):
        #if user does not have the permission node
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_image(url="https://imgur.com/nU9QbXv.png")
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        #if the command was missing arguments
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_image(url="https://imgur.com/tQzEKFv.png")
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        #other error
        else:
            print(error) # for other errors so they dont get suppressed

        
    @commands.has_permissions(ban_members=True)
    @commands.command(aliases = ["b"], brief="ban [@member name]",description="Perm ban a server member")
    async def ban(self, ctx, member:discord.Member, *, reason=None):
        if reason == None:
            reason = "No reason was provided."
    
        #embed to be displayed in the original context channel
        embed = discord.Embed(     
            title=f"{member.display_name} has been banned", 
            description = f"**User Tag:** {member.mention}\n\n**Banned By:** {ctx.author.mention}\n\n**Reason:** {reason}",
            colour = embed_color
            )
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url = "{}".format(member.avatar.url))
        embed.set_footer(text=f"©️ {member.guild.name}", icon_url = ctx.guild.icon.url)
        embed.set_image(url="https://imgur.com/7l8D0pZ.png")
        
        #embed to be displayed in the pushments priv channel
        priv_embed = discord.Embed( 
            title=f"{member.display_name} has been banned", 
            description = f"**User Tag:** {member.mention}\n\n**Reason:** {reason}",
            colour = embed_color
            )
        priv_embed.timestamp = datetime.datetime.now()
        priv_embed.set_thumbnail(url = "{}".format(member.avatar.url))
        priv_embed.set_footer(text = f"Banned by {ctx.author}", icon_url=ctx.author.avatar.url)
        
        await ctx.guild.ban(member)
        await self.client.get_channel(priv_staff_channel).send(embed=priv_embed)
        await ctx.send(embed=embed)
        
    @ban.error
    async def announcement_error(self, ctx, error):
        #if user does not have the permission node
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🔴 | No Permission",
                description="You are lacking permissions to perform this action. If you believe this to be a mistake, please contact a staff member.",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        #if the command was missing arguments
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="🔴 | Missing Arguments",
                description=f"The command you just ran is missing some arguments. Please use `{command_prefix}help` to double check the right command syntax.",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        #other error
        else:
            print(error) # for other errors so they dont get suppressed
            await ctx.send(error, "Please contact staff.")
        
async def setup(client):
    await client.add_cog(punishments(client))
    

