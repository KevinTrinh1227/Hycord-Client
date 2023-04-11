import discord
from discord.ext import commands
import discord.ui
import asyncio
import datetime
import json
import re

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

class announce(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #accouncement/say command
    @commands.has_permissions(administrator = True)
    @commands.command(aliases=["announcement", "an"], brief="announce", description="Create a fully costomizable embed message to send in a specific channel")
    async def announce(self, ctx):

        # Prompt the user for the channel they want to send the embed to
        await ctx.send("What channel should I send the embed to? (mention or name)")
        channel_response = await self.wait_for_message(ctx)

        # Try to get the specified channel
        if channel_response.content.startswith("#"):
            channel_name = channel_response.content[1:]
        else:
            channel_name = channel_response.content
        channel = discord.utils.get(ctx.guild.channels, name=channel_name.strip())
        if channel is None:
            await ctx.send("Sorry, I couldn't find that channel.")
            return

        # Prompt the user for the title of the embed
        await ctx.send("What should the title of the embed be?")
        title_response = await self.wait_for_message(ctx, timeout=60)

        # Prompt the user for the description of the embed
        await ctx.send("What should the description of the embed be?")
        description_response = await self.wait_for_message(ctx, timeout=60)

        # Prompt the user for the image URL of the embed
        await ctx.send("What should the image URL of the embed be? (or type N/A)")
        image_response = await self.wait_for_message(ctx, timeout=60)

        # Create the embed
        embed = discord.Embed(color = embed_color)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"© {ctx.guild.name}", icon_url = ctx.guild.icon.url)

        if title_response and title_response.content != "N/A":
            embed.title = title_response.content

        if description_response and description_response.content != "N/A":
            embed.description = description_response.content

        if image_response and image_response.content != "N/A":
            if self.is_valid_image_url(image_response.content):
                embed.set_image(url=image_response.content)
            else:
                await ctx.send("Sorry, that's not a valid image URL.")
                return

        # Send the embed to the specified channel
        await channel.send(embed=embed)


    # waiting for message time out
    async def wait_for_message(self, ctx, timeout=60):
        try:
            message = await self.client.wait_for("message", timeout=timeout, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long to respond.")
            return None
        return message

    # validating image url
    def is_valid_image_url(self, url):
        pattern = re.compile(r'\bhttps?://\S+(?:png|jpg|gif)\b', re.IGNORECASE)
        return bool(pattern.match(url))
        
        
    @announce.error
    async def ban_error(self, ctx, error):
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
        
        
async def setup(client):
    await client.add_cog(announce(client))