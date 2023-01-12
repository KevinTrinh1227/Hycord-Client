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
    

embed_color = data["embed_color"]
embed_color = int(data["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
    
    
class verify_mcaccount(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}
        try:
            with open("mc_accounts.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open("mc_accounts.json", "w") as f:
                json.dump({}, f)

    async def save_data(self):
        with open("mc_accounts.json", "w") as f:
            json.dump(self.data, f)
    
    #bedwars stats command
    @commands.command(aliases=["verify", "connect"], brief="link [Minecraft User Name]",description="link/verify your minecraft account")
    async def link(self, ctx, *, username):
        
        try: #if player exist it will work
            
            user_id = str(ctx.author.id)
            
            #if runs if user has already linked account
            if user_id in self.data:
                return await ctx.send("You have already linked your account.")
            
            #this else runs if user has not linked account
            else:  
                
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
                    guild_name = guild_data["guild"]["name"]
                except:
                    guild_name = "No Guild"
                
                #finding a players tier classification
                if bedwars_fkdr < 1:
                    classification_role_id = 1057348592978899004
                elif 1 <= bedwars_fkdr < 3:
                    classification_role_id = 1057332228906041364
                elif 3 <= bedwars_fkdr < 5:
                    classification_role_id = 1057330483811328000
                elif 5 <= bedwars_fkdr < 8:
                    classification_role_id = 1057027267903094868
                elif 8 <= bedwars_fkdr < 10:
                    classification_role_id = 1057027175544537199
                else: #fkdr 10+
                    classification_role_id = 1057027312014610553
                    
                
                classification_role = discord.utils.get(ctx.guild.roles, id=classification_role_id)
                unverified_role = discord.utils.get(ctx.guild.roles, id=934427489328062524)
                verified_linked_role = discord.utils.get(ctx.guild.roles, id=1057334059291906068)
                
                
                #check if the user even has social media activated
                if "socialMedia" in hydata["player"]:
                    #await ctx.send(f"User has a social media(s) connected.")
                    social_media = hydata["player"]["socialMedia"]["links"]
                    
                    #checks if user has Discord added
                    if "DISCORD" in social_media:
                        discord_tag = social_media["DISCORD"]
                        
                        #checks if both discord match
                        if str(ctx.author) == discord_tag:  
                            embed = discord.Embed(
                                title = f"**Successfully Verified Account** ✅",
                                url = f"https://plancke.io/hypixel/player/stats/{username}",
                                description = f"You have **seccessfully** linked your accounts. Based on your stats, you classify as a {role.mention}",
                                color = embed_color               
                            )
                            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                            embed.timestamp = datetime.datetime.now()
                            embed.add_field(name='IGN', value=username, inline=True)
                            embed.add_field(name='Level', value=f"{bedwars_level}✫", inline=True)
                            embed.add_field(name='Guild', value=guild_name, inline=True)
                            embed.add_field(name='Discord', value=ctx.author, inline=True)
                            embed.add_field(name='FKDR', value=bedwars_fkdr, inline=True)
                            embed.add_field(name='UUID', value=uuid, inline=True)
                            embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/128/{uuid}")
                            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                            
                            await ctx.author.edit(nick=new_nickname)    #change username of discord user to ingame name
                            await ctx.author.add_roles(classification_role, verified_linked_role)
                            await ctx.author.delete_roles(unverified_role)
                            await ctx.send(f"{guild_data['guild']['name']}")
                            await ctx.send(f"{ctx.author.mention}'s account is now linked and updated.", embed=embed)
                            await self.save_data() #save the json file
                            
                        #runs if discords do not match
                        else:
                            embed = discord.Embed (
                                title = f"**Failed | Accounts do not match** ❌",
                                description = f"The discord account connected to the hypixel user {username} does not match your current discord account. Try again.",
                                color = embed_color
                            )
                            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                            embed.timestamp = datetime.datetime.now()
                            embed.add_field(name='IGN', value=username, inline=True)
                            embed.add_field(name=f'{username}\'s Discord Tag', value=discord_tag, inline=True)
                            embed.add_field(name='Your Discord Tag', value=ctx.author, inline=True)
                            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                            await ctx.send(embed=embed)
                            
                    #runs if user has social media active but no discord
                    else:
                        embed = discord.Embed(
                            title = f"**Failed | Not connected in-game** ❌",
                            description = f"{username} does not have a Discord account linked yet. Be sure to link it in game first then run the command again.",
                            color = embed_color
                        )
                        embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                        embed.timestamp = datetime.datetime.now()
                        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                        await ctx.send(embed=embed)
                        
                #runs if user does not have social media active
                else:
                    embed = discord.Embed(
                        title = f"**Failed | Not connected in-game**",
                        description = f"{username} does not have a Discord account linked yet. Be sure to link it in game first then run the command again.",
                        color = embed_color
                    )
                    embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                    await ctx.send(embed=embed)
        
        except:
            embed = discord.Embed(
                title = f"User Does Not Exist",
                url = f"https://mcchecker.net/",
                description = f"Username: `{username}`\n\nThe username you have entered does not exist. Please check your spelling and try again. (You can use https://mcchecker.net/ to validate the username)",
                color = embed_color
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed)
        
        
async def setup(client):
    await client.add_cog(verify_mcaccount(client))        