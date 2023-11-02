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
    
class forceVerify(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}
        
    async def save_data(self):
        with open("verified_accounts.json", "w") as f:
            json.dump(self.data, f)
    
    
    @commands.has_permissions(administrator = True)
    @commands.hybrid_command(aliases=["flink", "fsync", "fverify"], brief="fsync [@member name] [Minecraft Username]", description="Force sync a user to a minecraft account", with_app_command=True)
    async def forceverify(self, ctx, user: discord.Member, username: str):
        
        #deletes the admin's command before executing
        # await ctx.channel.purge(limit = 1)
        
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
                title = f"**❌ | Your account is already linked**",
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
                
                # gets discord roles by ID
                unverified_role = discord.utils.get(ctx.guild.roles, id=unverified_role_id) #default role id
                verified_linked_role = discord.utils.get(ctx.guild.roles, id=verified_role_id) #verified role id
                guild_role = discord.utils.get(ctx.guild.roles, id=guild_role_id) #verified role id
                
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
                # print(guild_url)
                
                
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
                            await user.add_roles(verified_linked_role) # gives user guild role
                            
                        else:
                            pass
                            #print("Player is not in your guild!")
                            
                        
                    else:
                        guild_name = "Not in Guild"
                except Exception as error:
                    guild_name = "No Guild"
                    print("An error occurred:", error) # An error occurred: name 'x' is not defined
                
                """
                #embed message and linking step below
                embed = discord.Embed(
                    title = f"**✅ | Successfully Verified Account**",
                    url = f"https://plancke.io/hypixel/player/stats/{username}",
                    description = f"You have **successfully** linked your accounts.",
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
                """
                
                background_image = Image.open("./assets/backgrounds/560_250.png")
                overlay_image = Image.open("./assets/overlays/verification_success.png")
                
                try:
                    front_skin_url = f"https://visage.surgeplay.com/bust/{uuid}.png"
                    front_response = requests.get(front_skin_url)
                    front_skin = Image.open(BytesIO(front_response.content))
                except:
                    front_skin = Image.open("./assets/resources/default_skin_front.png")
                    
                    
                front_skin = front_skin.resize((151, 124))
                background_image.paste(overlay_image, (0, 0), overlay_image)
                background_image.paste(front_skin, (16, 68), front_skin)
                
                text1 = "Verification Success"
                text2 = f"{ctx.guild.name} | Hycord.net"
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
                draw.text((306,92), user.name, (255, 255, 255), font=font_footer)
                draw.text((250,167), str(bedwars_fkdr), (255, 255, 255), font=font_footer)
                draw.text((257,142), str(bedwars_level), (255, 255, 255), font=font_footer)
                draw.text((252,117), guild_name, (255, 255, 255), font=font_footer)
                background_image.save("./assets/outputs/verified.png") # save the img
                
                self.data[user_id] = {
                    "uuid":uuid,
                    "username":ign
                    }
                await self.save_data()
                with open('verified_accounts.json', 'w') as f:
                    json.dump(self.data, f, indent=4)
                
                #modifies user's roles and nickname
                await user.edit(nick=new_nickname)
                await user.add_roles(verified_linked_role)
                await user.remove_roles(unverified_role)
                #await ctx.send(f"{user.mention}'s account is now linked and updated.", embed=embed)
                await ctx.send(f"{user.mention} account is now linked and updated.", file=discord.File("./assets/outputs/verified.png"))
                
            #runs if user does not exist
            except Exception as e:
                error_message = str(e)
                print("ERROR:", error_message)
                embed = discord.Embed(
                    title = f"An Error Occured",
                    description = f"An error occured during the linking process. Either the user: `{username}` does not exist, OR your Hypixel API key is invalid. Please double check",
                    color = embed_color
                )
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
                
                await ctx.send(embed=embed)
                

async def setup(client):
    await client.add_cog(forceVerify(client))