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

command_prefix = data["general"]["bot_prefix"]
embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

class announce(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #accouncement/say command
    @commands.has_permissions(administrator = True)
    @commands.hybrid_command(aliases=["announcement", "an"], brief="announce", description="Create a fully customizable embed message to send in a specific channel", with_app_command=True)
    async def announce(self, ctx):

        try:
            # Prompt the user to select a channel
            await ctx.send("What channel would you like to post the embed in? Please mention the channel or provide the channel ID.")
            # Wait for the user's response
            try:
                msg = await self.client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you took too long to respond. Please try again.")
                return
            # Try to convert the response into a channel object
            try:
                channel = await commands.TextChannelConverter().convert(ctx, msg.content)
            except commands.errors.ChannelNotFound:
                channel = None
            # If the channel is not valid, send an error message
            if not channel:
                await ctx.send("Sorry, I couldn't find that channel. Please try again.")
                return
            # Prompt the user to enter the embed title (optional)
            await ctx.send("What would you like the title of the embed to be? Type 'skip' to skip this step.")
            # Wait for the user's response
            try:
                msg = await self.client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you took too long to respond. Please try again.")
                return
            title = msg.content if msg.content != "skip" else None
            # Prompt the user to enter the embed description (optional)
            await ctx.send("What would you like the description of the embed to be? Type 'skip' to skip this step.")
            # Wait for the user's response
            try:
                msg = await self.client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=240.0)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you took too long to respond. Please try again.")
                return
            description = msg.content if msg.content != "skip" else None
            # Prompt the user to enter the embed image URL (optional)
            await ctx.send("Do you have an image URL for the embed? Please provide the link, or type 'skip' to skip this step.")
            # Wait for the user's response
            try:
                msg = await self.client.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you took too long to respond. Please try again.")
                return
            image_url = msg.content
            # If the user provided an image URL, add it to the embed
            if image_url != "skip":
                embed = discord.Embed(color=embed_color)
                if title:
                    embed.title = title
                if description:
                    embed.description = description
                embed.set_image(url=image_url)
            else:
                embed = discord.Embed(color=embed_color)
                if title:
                    embed.title = title
                if description:
                    embed.description = description
            # Send the embed to the selected channel
            await channel.send(embed=embed)
            await ctx.send(f"The following embed has been posted in {channel.mention}.")
            await ctx.send(embed=embed)
        except:
            await ctx.send("You have skipped all input fields. Try again!")
        
        
async def setup(client):
    await client.add_cog(announce(client))