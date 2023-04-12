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

    
class bwstats(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #bedwars stats command
    @commands.command(aliases=["bedwarsstats", "bwstat", "bws"], brief="bws [Minecraft User Name]",description="View a players Bedwars Stats")
    async def bwstats(self, ctx, *, username):
        
        try:#if player exist it will work
            
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
            bedwars_final_deaths = hydata['player']['stats']['Bedwars']["final_deaths_bedwars"]
            bedwars_fkdr = round((bedwars_final_kills/bedwars_final_deaths), 2)
            
            #finals stats
            bedwars_kills = hydata["player"]["stats"]["Bedwars"]["kills_bedwars"]
            bedwars_deaths = hydata['player']['stats']['Bedwars']["deaths_bedwars"]
            bedwars_kdr = round((bedwars_kills/bedwars_deaths), 2)
            
            #beds broken stats
            bedwars_beds_broken = hydata['player']['stats']["Bedwars"]["beds_broken_bedwars"]
            bedwars_beds_lost = hydata['player']['stats']["Bedwars"]["beds_lost_bedwars"]
            bedwars_bed_bblr = round((bedwars_beds_broken/bedwars_beds_lost), 2)
            
            #wins and losses
            bedwars_wins = hydata['player']['stats']['Bedwars']["wins_bedwars"]
            bedwars_losses = hydata['player']['stats']['Bedwars']["losses_bedwars"]
            bedwars_wlr = round((bedwars_wins/bedwars_losses), 2)
            
            #other statistics
            bedwars_level = hydata["player"]["achievements"]["bedwars_level"] #bedwars level
            
            #player embed
            embed = discord.Embed(
                title = f"**General Bedwars Stats**",
                url = f"https://plancke.io/hypixel/player/stats/{username}",
                description = f"**Level: **✫{bedwars_level}\n**UUID:** `{uuid}`",
                color = embed_color
            )
            embed.set_author(name = f"{username}'s Profile", icon_url = f"https://crafatar.com/avatars/{uuid}")
            embed.timestamp = datetime.datetime.now()
            embed.add_field(name='Final Kills', value=bedwars_final_kills, inline=True)
            embed.add_field(name='Final Deaths', value=bedwars_final_deaths, inline=True)
            embed.add_field(name='FKDR', value=bedwars_fkdr, inline=True)
            embed.add_field(name='Wins', value=bedwars_wins, inline=True)
            embed.add_field(name='Losses', value=bedwars_losses, inline=True)
            embed.add_field(name='WLR', value=bedwars_wlr, inline=True)
            embed.add_field(name='Beds Broken', value=bedwars_wins, inline=True)
            embed.add_field(name='Beds Lost', value=bedwars_beds_lost, inline=True)
            embed.add_field(name='BBLR', value=bedwars_bed_bblr, inline=True)
            embed.add_field(name='Kills', value=bedwars_kills, inline=True)
            embed.add_field(name='Deaths', value=bedwars_deaths, inline=True)
            embed.add_field(name='KDR', value=bedwars_kdr, inline=True)
            embed.set_thumbnail(url = f"https://visage.surgeplay.com/bust/128/{uuid}")
            embed.set_footer(text = f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed)
        except:     #if player does not exist
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
    await client.add_cog(bwstats(client))