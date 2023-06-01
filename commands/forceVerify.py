import discord
from discord.ext import commands
import requests
import discord.ui
import datetime
import json
import os
from dotenv import load_dotenv

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
unverified_role_id = int(data["role_ids"]["unverified_member"])
verified_role_id = int(data["role_ids"]["verified_member"])
    
    
class forceVerify(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}
        
    async def save_data(self):
        with open("verified_accounts.json", "w") as f:
            json.dump(self.data, f)
    
    
    @commands.has_permissions(administrator = True)
    @commands.command(aliases=["flink", "fsync", "fverify"], brief="fsync [@member name] [Minecraft Username]",description="Force sync a user to a minecraft account")
    async def forceVerify(self, ctx, user: discord.Member, username: str):
        
        #deletes the admin's command before executing
        await ctx.channel.purge(limit = 1)
        
        try:
            with open("verified_accounts.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open("verified_accounts.json", "w") as f:
                json.dump({}, f)
                
        #user ID is equal to the mentioned user's ID
        user_id = str(user.id)
        #if user has already linked
        if user_id in self.data:
            
            existing_uuid = self.data[user_id]["uuid"]
            
            embed = discord.Embed(
                title = f"**Your account is already linked**  ❌",
                url = f"https://plancke.io/hypixel/player/stats/{existing_uuid}",
                description = f"**UUID:** `{existing_uuid}`\n\nYou already have an account linked to this discord. Please use `!unverify` to unlink your account then try again.",
                color = embed_color
            )
            embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/128/{existing_uuid}")
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
            await ctx.send(embed=embed)
                
        else:
            try: #if player exist it will work
                
                #load in .env variables
                load_dotenv() 

                #get hypixel api key
                hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
                
                url = f"https://api.mojang.com/users/profiles/minecraft/{username}?"
                response = requests.get(url)
                uuid = response.json()['id']

                requestlink = f"https://api.hypixel.net/player?key={hypixel_api_key}&uuid={uuid}"
                hydata = requests.get(requestlink).json()
                
                #finals stats
                bedwars_final_kills = hydata["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
                bedwars_final_deaths = hydata["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
                bedwars_fkdr = round((bedwars_final_kills/bedwars_final_deaths), 2)
            
                #other bedwars stats
                bedwars_level = hydata["player"]["achievements"]["bedwars_level"] #bedwars level
                new_nickname = f"[{bedwars_level}✫] {username}"
                
                #user guild information
                guild_url = f"https://api.hypixel.net/guild?player={uuid}&key={hypixel_api_key}"
                guild_response = requests.get(guild_url)
                guild_data = guild_response.json()
                
                #checks if user is in a guild
                try:
                    if "name" in guild_data["guild"]:
                        guild_name = guild_data["guild"]["name"]
                    else:
                        guild_name = "Not in Guild"
                except: #runs if player is not in a guild
                    guild_name = "No Guild"
            
                
                unverified_role = discord.utils.get(ctx.guild.roles, id=unverified_role_id) #default role id
                verified_linked_role = discord.utils.get(ctx.guild.roles, id=verified_role_id) #verified role id
                
                #embed message and linking step below
                embed = discord.Embed(
                    title = f"**Successfully Verified Account** ✅",
                    url = f"https://plancke.io/hypixel/player/stats/{username}",
                    description = f"You have **seccessfully** linked your accounts.",
                    color = embed_color               
                )
                embed.timestamp = datetime.datetime.now()
                embed.add_field(name='IGN', value=username, inline=True)
                embed.add_field(name='Level', value=f"{bedwars_level}✫", inline=True)
                embed.add_field(name='Guild', value=guild_name, inline=True)
                embed.add_field(name='Discord', value=user, inline=True)
                embed.add_field(name='FKDR', value=bedwars_fkdr, inline=True)
                embed.add_field(name='UUID', value=uuid, inline=True)
                embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/128/{uuid}")
                embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                
                self.data[user_id] = {
                    "uuid":uuid, 
                    }
                await self.save_data()
                with open('verified_accounts.json', 'w') as f:
                    json.dump(self.data, f, indent=4)
                
                #modifies user's roles and nickname
                await user.edit(nick=new_nickname)
                await user.add_roles(verified_linked_role)
                await user.remove_roles(unverified_role)
                await ctx.send(f"{user.mention}'s account is now linked and updated.", embed=embed)
                
            #runs if user does not exist
            except:
                embed = discord.Embed(
                    title = f"User Does Not Exist",
                    url = f"https://mcchecker.net/",
                    description = f"Username: `{username}`\n\nThe username you have entered does not exist. Please check your spelling and try again. (You can use https://mcchecker.net/ to validate the username)",
                    color = embed_color
                )
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text = f"Account of {user.author}", icon_url=user.avatar.url)
                
                await ctx.send(embed=embed)
                

async def setup(client):
    await client.add_cog(forceVerify(client))