import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime
import discord.ui
import json


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = data["embed_color"]
embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format


class unverify(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["unverify", "unconnect"], brief="unlink",description="unsync your minecraft account")
    async def unlink(self, ctx):
        member = ctx.message.author
        with open('verified_accounts.json', 'r') as f:
            verified_accounts = json.load(f)

        if str(member.id) in verified_accounts:
            del verified_accounts[str(member.id)]

            with open('verified_accounts.json', 'w') as f:
                json.dump(verified_accounts, f, indent=4)
            await member.edit(nick=None) # This line will reset the user's nickname
            await ctx.send(f'{ctx.author} has been removed from the verified accounts list.')
        else:
            await ctx.send(f'{ctx.author} was not found in the verified accounts list.')
        
        
async def setup(client):
    await client.add_cog(unverify(client))
    

