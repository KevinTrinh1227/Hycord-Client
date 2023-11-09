import discord
from discord.ext import commands
from discord.ext import tasks
import discord.ui
import json
import datetime

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
logs_channel_id = int(data["text_channel_ids"]["bot_logs"])    # logs the bot logs in this channel


class general_logs(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
            deleter = entry.user
            
            #print(entry)
            #print(message)
        
            channel = self.client.get_channel(logs_channel_id)
        
            embed = discord.Embed(
                title=(f"🗑️ | A message was deleted in #{message.channel.name}"),
                description=f"**Message deleted:** ```{message.content}```",
                colour= embed_color
                )
            embed.set_author(name=f"{deleter.name} ({deleter.display_name})", icon_url=deleter.avatar.url)
            embed.add_field(name="Message Author", value=message.author.mention,
                            inline=True)
            embed.add_field(name="Author Name", value=message.author.name,
                            inline=True)
            embed.add_field(name="Author ID", value=message.author.id,
                            inline=True)
            
            embed.add_field(name="Deleter", value=deleter.mention,
                            inline=True)
            embed.add_field(name="Deleter Name", value=deleter.name,
                            inline=True)
            embed.add_field(name="Deleter ID", value=deleter.id,
                            inline=True)

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        embed = discord.Embed(
            title=f"✂️ | A message was edited in #{message_before.channel.name}",
            description=f"**Old Message:**\n```{message_before.content}```\n**New Message:**\n```{message_after.content} ```",
            color=0xFF0000
            )
        embed.set_author(name=f"{message_before.author.name} ({message_before.author.display_name})", icon_url=message_before.author.avatar.url)
        embed.add_field(name="Message Author", value=message_before.author.mention,
                        inline=True)
        embed.add_field(name="Author Name", value=message_before.author.name,
                        inline=True)
        embed.add_field(name="Author ID", value=message_before.author.id,
                        inline=True)
        
        channel = self.client.get_channel(logs_channel_id)
        
        await channel.send(channel, embed=embed)

async def setup(client):
    await client.add_cog(general_logs(client))
