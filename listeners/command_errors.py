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


class commend_error(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # ERROR: if command doesnt exist
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title=(f"**🔎 | Command does not exist!**"),
                description=f"The command you just issued does not exist. Please use `{bot_prefix}help` to double check the correct syntax. Contact staff if this is a mistake.",
                colour= embed_color
                )
            embed.timestamp = datetime.datetime.now()
            if(ctx.author.avatar):  # if user does have an avatar
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
            else:                   # if user DOES NOT have an avatar
                embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)

        # ERROR: if user has a command cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title=(f"⏳ ** | This command is on cooldown!**"),
                description=f"Please wait `{error.retry_after:.2f}` more second(s) before trying to run the command again. If you believe this to be a mistake, please contact a staff member.",
                colour= embed_color
                )
            embed.timestamp = datetime.datetime.now()
            if(ctx.author.avatar):  # if user does have an avatar
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
            else:                   # if user DOES NOT have an avatar
                embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)
        # ERROR: if user does not have the permission node
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫** | You are lacking permissions!**",
                description="You are lacking permissions to perform this action. If you believe this to be a mistake, please contact a staff member.",
                color = embed_color

            )
            embed.timestamp = datetime.datetime.now()
            if(ctx.author.avatar):  # if user does have an avatar
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
            else:                   # if user DOES NOT have an avatar
                embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)
        # ERROR: if the command was missing arguments
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="🟡** | Missing arguments in command.**",
                description=f"The command you just ran is missing one or more arguments. Please use `{bot_prefix}help` to double check the command syntax, and try again.",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            if(ctx.author.avatar):  # if user does have an avatar
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
            else:                   # if user DOES NOT have an avatar
                embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)
        else:
            print(error) # for other errors so they dont get suppressed
            await ctx.send("An error has occured, please contact the bot dev.")


    
        
async def setup(client):
    await client.add_cog(commend_error(client))
    
    

