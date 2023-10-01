import discord
from discord.ext import commands
import datetime
import discord.ui
import json


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
verified_role_id = int(data["role_ids"]["verified_member"])
unverified_role_id = int(data["role_ids"]["unverified_member"])


class forceunverify(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.has_permissions(administrator = True)
    @commands.hybrid_command(aliases=["funverify", "disconnect", "funlink", "delink"], brief="delink @[Mention Member]", description="unsync a user's account", with_app_command=True)
    async def forceunverify(self, ctx, user: discord.Member):
        member = user
        with open('verified_accounts.json', 'r') as f:
            verified_accounts = json.load(f)
            
        try:
            if str(member.id) in verified_accounts:
                
                #get the user's uuid from verified_accounts.json
                uuid = verified_accounts[str(member.id)]["uuid"]
                
                #deletes the user from the json file
                del verified_accounts[str(member.id)]

                #formats the json file to look pretty
                with open('verified_accounts.json', 'w') as f:
                    json.dump(verified_accounts, f, indent=4)
                    
                #removing roles from the user unlinking accounts
                unverified_role = discord.utils.get(ctx.guild.roles, id=unverified_role_id)
                try:
                    user_role_ids = [role.id for role in member.roles]
                    role_ids_to_check = [verified_role_id]
                    role_ids_to_remove = [role_id for role_id in user_role_ids if role_id in role_ids_to_check]
                    for role_id in role_ids_to_remove:
                        role = discord.utils.get(ctx.guild.roles, id=role_id)
                        await member.remove_roles(role)
                except:
                    pass
                    
                embed = discord.Embed(
                    title = f"**Successfully unlinked account!** ✅",
                    description = f"The Discord account `{user}` is now unlinked. Relink your account to claim your roles again!",
                    color = embed_color
                )
                embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/128/{uuid}")
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                
                await user.add_roles(unverified_role) #give the unverified role
                await member.edit(nick=None) # This line will reset the user's nickname
                await ctx.send(embed=embed)
                
                
            else:
                embed = discord.Embed(
                    title = f"**Failed to unlink account!** ❌",
                    description = f"{user} was not found in the verified accounts list. Please link your account first before trying this command.",
                    color = embed_color
                )
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                await ctx.send(embed=embed)

        except:
            embed = discord.Embed(
                title = f"**⚠️ | Error occured**",
                description = f"An error occured during the prcoess. Please make sure the bot has a higher role priority for this command to work. Note that the bot won't be able to perform this command on server server owner's, and users with roles that are of higher priority.",
                color = embed_color
            )
            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
            await ctx.send(embed=embed)
        
async def setup(client):
    await client.add_cog(forceunverify(client))