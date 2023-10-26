import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import json
import discord
import requests
import discord.ui
import os
from dotenv import load_dotenv
import asyncio
import time
import utils.guild_data as guild

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
hypixel_guild_id = data["hypixel_ids"]["guild_id"]


class guildList(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.guild_id = hypixel_guild_id
    
    @commands.hybrid_command(aliases = ["gl", "guildl"], brief="guildlist", description="Displays list of all guild members", with_app_command=True)
    @commands.cooldown(1, 120, commands.BucketType.user) # 2 min cool down.
    async def guildlist(self, ctx):
        
        
        try:
                
            hypixel_api_key = os.getenv("HYPIXEL_API_KEY")
            api_link = f'https://api.hypixel.net/guild?key={hypixel_api_key}&id={hypixel_guild_id}'
            response = requests.get(api_link)
            
            # Record the start time
            start_time = time.time()

            if response.status_code == 200:
                data = response.json()
                members = data['guild']['members']
                guild_name = data['guild']['name']
                
                output = ""
                total_members = len(members)
                total_time = 0
                page_size = 25
                
                total_pages = total_members // page_size
                if total_members % page_size != 0:
                    total_pages += 1
                
                await ctx.send(f"Now fetching {guild_name}'s data. Estimated wait time: `{(total_members * 2):.0f}` seconds.")
                
                
                for idx, member in enumerate(members):
                    uuid = member["uuid"]
                    
                    user_name = guild.search_uuid_and_return_name("guild_cache.json", uuid)
                    
                    if user_name == None:
                        user_name = uuid
                    else:
                        pass
                    
                    
                    current_time = int(time.time() * 1000)
                    member_age_ms = current_time - member["joined"]
                    member_age_days = member_age_ms / (1000 * 60 * 60 * 24)
                    total_time += member_age_days
                    
                    if idx % page_size == 0:
                        if idx > 0:
                            #print(f"Page {idx // page_size + 1}:")
                            #print(output)  # Print previous 25 players
                            # Record the end time
                            end_time = time.time()
                            # Calculate the elapsed time
                            elapsed_time = end_time - start_time
                            #print(f"Elapsed time: {elapsed_time:.2f} seconds")
                            
                            embed = discord.Embed(
                                title = f"**📝 | {guild_name} Guild Roster [{idx // page_size}/{total_pages}]**", 
                                description=f"""
                                You guild has `{total_members}`/`125` members. `{125 - total_members}` Empty slots.
                                {output}
                                
                                Days represents time in guild. Page: `{idx // page_size}/{total_pages}`
                                """,
                                colour = embed_color
                                )
                            #embed.set_thumbnail(url = "{}".format(ctx.guild.icon.url)),
                            embed.timestamp = datetime.now()
                            embed.set_footer(text=f"©️ {ctx.guild.name} | {elapsed_time:.0f}s", icon_url = ctx.guild.icon.url)
                            await ctx.send(embed=embed)
                        output = ""

                    output += f"\n**{idx + 1}.** [{user_name}](https://plancke.io/hypixel/player/stats/{uuid}) - `{member_age_days:.2f} days`"
                    #print(f"\n**{idx + 1}.** [{user_name}](https://plancke.io/hypixel/player/stats/{uuid}) - `{member_age_days:.2f} days`")

                # After the loop, print any remaining players
                if output:
                    end_time = time.time()
                    # Calculate the elapsed time
                    elapsed_time = end_time - start_time
                    #print(f"Elapsed time: {elapsed_time:.2f} seconds")
                    #print(f"Page {idx // page_size + 1}:")
                    #print(output)
                    embed = discord.Embed(
                        title = f"**📝 | {guild_name} Guild Roster [{idx // page_size + 1}/{total_pages}]**", 
                        description=f"""
                        You guild has `{total_members}`/`125` members. `{125 - total_members}` Empty slots.
                        {output}
                        
                        Days represents time in guild. Page: `{idx // page_size + 1}/{total_pages}`
                        """,
                        colour = embed_color
                        )
                    #embed.set_thumbnail(url = "{}".format(ctx.guild.icon.url)),
                    embed.timestamp = datetime.now()
                    embed.set_footer(text=f"©️ {ctx.guild.name} | {elapsed_time:.0f}s", icon_url = ctx.guild.icon.url)
                    await ctx.send(embed=embed)
                
            
        except Exception as e:
            error_message = str(e)
            await ctx.send(f"There was an error: {error_message}. Please double-check your Guild ID and Hypixel API key.")

        
async def setup(client):
    await client.add_cog(guildList(client))
    

