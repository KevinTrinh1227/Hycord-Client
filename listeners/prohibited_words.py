import discord
import requests
from discord.ext import commands
import json
import datetime

""" ==========================================
* CHAT FILTER FEATURE
*
* Note that this feature uses a super strict
* profanity checker system through API.
* I recommend only using this feature if you
* have a PG discord server community.

* IMPORTANT: This feature only applies to messages
* under 4096 characters. Otherwise it will ignore
* any and all messages over that limit.
========================================== """

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

class BadWordCheck(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return  # ignore messages sent by the bot itself

        # Reopen the JSON file to read it again
        with open('config.json') as json_file:
            cdata = json.load(json_file)
        if bool(cdata["features"]["filtered_chat"]):

            content = message.content.lower()
            bad_word = self.check_profanity(content)

            if bad_word:
                guild = message.guild #getting guild

                spoilered_message = f"||{message.content.replace(bad_word, f'__{bad_word}__')}||"
        
                embed = discord.Embed(
                    title=f"**Prohibited Word Warning | {message.author}**",
                    description=f"""
                    Your message was deleted because it contained prohibited words. You can ignore this message if it was a mistake.
                    
                    **Filtered Message:** `{bad_word}`
                    
                    Please refrain from using any harmful content to avoid being punished. User: {message.author.mention}
                    """,
                    color=embed_color
                ) # OPTIONAL: **Original Message:** {spoilered_message}
                if message.author.avatar:
                    embed.set_thumbnail(url=message.author.avatar.url)
                #else:
                    #embed.set_thumbnail(url=message.author.guild.icon.url)
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text=f"© {guild.name}", icon_url=guild.icon.url)

                await message.delete()
                await message.channel.send(embed=embed)

        # filtered chat is disabled
        else:
            return

    def check_profanity(self, text):
        if len(text) > 4096:
            return None
        
        url = f"https://www.purgomalum.com/service/containsprofanity?text={text}"
        response = requests.get(url)
        if response.text.lower() == "true":
            url = f"https://www.purgomalum.com/service/json?text={text}"
            response = requests.get(url)
            data = response.json()
            return data["result"]
        else:
            return None


async def setup(client):
    await client.add_cog(BadWordCheck(client))
