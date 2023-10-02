import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    
#json data to run bot
bot_prefix = data["general"]["bot_prefix"]
embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
leave_channel_id = int(data["text_channel_ids"]["leave_messages"])
member_role_id = int(data["role_ids"]["unverified_member"])
welcome_channel_id = int(data["text_channel_ids"]["welcome"])


class joinleave(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        
    #on member join event        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        #Auto role feature
        role = member.guild.get_role(member_role_id) #ID of normal member role
        roleStr = str(role)
        autoRole = discord.utils.get(member.guild.roles, name = roleStr)
        #welcome embed
        member_count = len(member.guild.members)
        channel = self.client.get_channel(welcome_channel_id)
        embed = discord.Embed(
            title=(f"Welcome to {member.guild.name} (#{member_count})"),
            description = f"""
            Welcome to the {member.guild.name}! Verify your account using `{bot_prefix}link [your IGN]`.

            *THIS IS A PLACEHOLDER WELCOME MESSAGE
            YOU CAN EDIT THIS IN "~/Hycord-Bot/client.py"*

            Member: {member.mention} 
            """,
            colour= embed_color
            )
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url = "{}".format(member.avatar.url))
        #embed.set_image(url="https://imgur.com/btR7AnN.png")
        embed.set_footer(text=f"©️ {member.guild.name}", icon_url = member.guild.icon.url)
        await channel.send(f"||{member.mention}||")
        await channel.purge(limit = 1)
        await channel.send(embed=embed)
        await member.add_roles(autoRole)
    

    # on member leave event
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        
        channel = self.client.get_channel(leave_channel_id)
        embed = discord.Embed(
            title=(f"{member.display_name}#{member.discriminator} has left the server."),
            description=f"{member.mention} has left {member.guild.name}.",
            colour= embed_color
            )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"©️ {member.guild.name}", icon_url = member.guild.icon.url)
        await channel.send(embed=embed)


    
        
async def setup(client):
    await client.add_cog(joinleave(client))
    
    

