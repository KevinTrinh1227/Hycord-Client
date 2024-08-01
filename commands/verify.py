import discord
from discord.ext import commands
import requests
import discord.ui
import datetime
import json
import os
from dotenv import load_dotenv
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests


# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
unverified_role_id = int(data["role_ids"]["unverified_member"])
verified_role_id = int(data["role_ids"]["verified_member"])
guild_role_id = int(data["role_ids"]["guild_member"])
font_title = ImageFont.truetype("./assets/fonts/Minecraft.ttf", 16)
font_footer = ImageFont.truetype("./assets/fonts/Minecraft.ttf", 13)

hypixel_guild_id = data["hypixel_ids"]["guild_id"]
verification_template = data["embed_templates"]["verification_nickname"]
    
    
class verify_mcaccount(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}

    async def save_data(self):
        with open("verified_accounts.json", "w") as f:
            json.dump(self.data, f)
            
            
    #bedwars stats command
    @commands.hybrid_command(aliases=["sync", "connect", "link"], brief="verify [Minecraft User Name]",description="sync/verify your minecraft account", with_app_command=True)
    @commands.cooldown(1, 20, commands.BucketType.user) # 20 sec cool down.
    async def verify(self, ctx, *, username):
        
        try:
            with open("verified_accounts.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open("verified_accounts.json", "w") as f:
                json.dump({}, f)
        
        user_id = str(ctx.author.id)
        if user_id in self.data:
            
            existing_uuid = self.data[user_id]["uuid"]
            
            embed = discord.Embed(
                title = f"**Your account is already linked**  ❌",
                url = f"https://plancke.io/hypixel/player/stats/{existing_uuid}",
                description = f"**UUID:** `{existing_uuid}`\n\nYou already have an account linked to this discord. Please use `!unverify` to unlink your account then try again.",
                color = embed_color
            )
            embed.set_author(name = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
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
                ign = response.json()['name']

                requestlink = f"https://api.hypixel.net/player?key={hypixel_api_key}&uuid={uuid}"
                hydata = requests.get(requestlink).json()
                
                #finals stats
                bedwars_final_kills = hydata["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
                bedwars_final_deaths = hydata["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
                bedwars_fkdr = round((bedwars_final_kills/bedwars_final_deaths), 2)
            
                #other bedwars stats
                bedwars_level = hydata["player"]["achievements"]["bedwars_level"] #bedwars level
                
                # default for users not in the server guild
                new_nickname = verification_template["verified_non_guild_member"].format(
                    ign = ign
                )
                
                #user guild information
                guild_url = f"https://api.hypixel.net/guild?player={uuid}&key={hypixel_api_key}"
                guild_response = requests.get(guild_url)
                guild_data = guild_response.json()
                
                unverified_role = discord.utils.get(ctx.guild.roles, id=unverified_role_id) #default role id
                verified_linked_role = discord.utils.get(ctx.guild.roles, id=verified_role_id) #verified role id
                guild_role = discord.utils.get(ctx.guild.roles, id=guild_role_id) #verified role id
                
                #checks if user is in a guild
                try:
                    for member in guild_data["guild"]["members"]:
                        if member.get("uuid") == uuid:
                            member_data = member
                            user_rank = member_data.get("rank") # guild rank/role
                            # print(user_rank)

                    if "name" in guild_data["guild"]:
                        guild_name = guild_data["guild"]["name"]
                        guild_id = guild_data["guild"]["_id"]
                        
                        if guild_id == hypixel_guild_id:
                            # print("This user is in your guild!")
                            
                            new_nickname = verification_template["verified_guild_member"].format(
                                ign = ign,
                                guild_rank = user_rank
                            )
                            await ctx.author.add_roles(guild_role) # gives user guild role
                            
                        else:
                            pass
                            #print("Player is not in your guild!")
                            
                        
                    else:
                        guild_name = "Not in Guild"
                except Exception as error:
                    guild_name = "No Guild"
                    #print("An error occurred:", error) # An error occurred: name 'x' is not defined
                
                
                #check if the user even has social media activated
                if "socialMedia" in hydata["player"]:
                    #await ctx.send(f"User has a social media(s) connected.")
                    social_media = hydata["player"]["socialMedia"]["links"]
                    
                    #checks if user has Discord added
                    if "DISCORD" in social_media:
                        discord_tag = social_media["DISCORD"]
                        
                        
                        #checks if both discord match
                        if str(ctx.author) == discord_tag:  
                            
                            """
                            embed = discord.Embed(
                                title = f"**Successfully Verified Account** ✅",
                                url = f"https://plancke.io/hypixel/player/stats/{username}",
                                description = f"You have **successfully** linked your accounts.",
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
                            """
                            
                            background_image = Image.open("./assets/backgrounds/560_250.png")
                            overlay_image = Image.open("./assets/overlays/verification_success.png")
                            
                            try:
                                front_skin_url = f"https://visage.surgeplay.com/bust/{uuid}.png"
                                headers = {
                                    "User-Agent": "HycordBot/2.0 (+https://github.com/KevinTrinh1227/Hycord-Client; https://kevintrinh.dev)"
                                }
                                front_response = requests.get(front_skin_url, headers=headers)
                                front_response.raise_for_status()  # This will raise an error for HTTP errors
                                front_skin = Image.open(BytesIO(front_response.content))
                            except:
                                front_skin = Image.open("./assets/resources/default_skin_front.png")
                                
                                
                            front_skin = front_skin.resize((151, 124))
                            background_image.paste(overlay_image, (0, 0), overlay_image)
                            background_image.paste(front_skin, (16, 68), front_skin)
                            
                            text1 = "Verification Success"
                            text2 = f"© {ctx.guild.name} | Hycord.net"
                            text3 = f"Username:"
                            text4 = f"Discord Tag:"
                            text5 = f"Guild:"
                            text6 = f"Level:"
                            text7 = f"FKDR:"
                            
                            draw = ImageDraw.Draw(background_image)
                            
                            _, _, text1_width, _ = draw.textbbox((0, 0), text1, font=font_title)
                            _, _, text2_width, _ = draw.textbbox((0, 0), text2, font=font_footer)
                            
                            image_width, _ = background_image.size
                            center_x1 = (image_width - text1_width) // 2
                            center_x2 = (image_width - text2_width) // 2
                            
                            draw = ImageDraw.Draw(background_image)
                            draw.text((center_x1,20), text1, (85, 255, 85), font=font_title)
                            draw.text((center_x2,212), text2, (255, 255, 255), font=font_footer)
                            draw.text((205,67), text3, (255, 255, 85), font=font_footer)
                            draw.text((205,92), text4, (255, 255, 85), font=font_footer)
                            draw.text((205,117), text5, (255, 255, 85), font=font_footer)
                            draw.text((205,142), text6, (255, 255, 85), font=font_footer)
                            draw.text((205,167), text7, (255, 255, 85), font=font_footer)

                            draw.text((293,67), ign, (255, 255, 255), font=font_footer)
                            draw.text((306,92), ctx.author.name, (255, 255, 255), font=font_footer)
                            draw.text((250,167), str(bedwars_fkdr), (255, 255, 255), font=font_footer)
                            draw.text((257,142), str(bedwars_level), (255, 255, 255), font=font_footer)
                            draw.text((252,117), guild_name, (255, 255, 255), font=font_footer)
                            background_image.save("./assets/outputs/verified.png") # save the img

                            # await ctx.send(f"{ctx.author.mention} account is now linked and updated.", file=discord.File("./assets/outputs/verified.png"))
                            
                            self.data[user_id] = {
                                "uuid":uuid,
                                "username":ign
                                }
                            await self.save_data()
                            with open('verified_accounts.json', 'w') as f:
                                json.dump(self.data, f, indent=4)
                            
                            #modifies user's roles and nickname
                            try:
                                await ctx.author.edit(nick=new_nickname)
                            except:
                                await ctx.send("Verification was a success, but the bot could not change the user's nickname. This means the user is the server owner, or they have a higher role priority than the bot.")
                            await ctx.author.add_roles(verified_linked_role)
                            await ctx.author.remove_roles(unverified_role)
                            #await ctx.send(f"{ctx.author.mention}'s account is now linked and updated.", embed=embed)
                            await ctx.send(f"{ctx.author.mention} account is now linked and updated.", file=discord.File("./assets/outputs/verified.png"))
                            
                            
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
                    
            except Exception as e:
                error_message = str(e)
                print("ERROR:", error_message)
                
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