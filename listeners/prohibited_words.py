import discord
import requests
from discord.ext import commands
import json
import datetime

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
rules_channel = int(data["text_channel_ids"]["rules"])

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
        if cdata["general"]["filtered_chat"] == "True":

            content = message.content.lower()
            bad_word = self.check_profanity(content)

            if bad_word:
                guild = message.guild #getting guild

                spoilered_message = f"||{message.content.replace(bad_word, f'__**{bad_word}**__')}||"

                rule_channel_obj = message.guild.get_channel(rules_channel)

                embed = discord.Embed(
                    title=f"**Prohibited Word Warning | {message.author}**",
                    description=f"""
                    Your message was deleted because it contained prohibited words. You can ignore this message if it was a mistake.
                    
                    **User: **{message.author.mention}
                    
                    **Filtered Message: **{bad_word}
                    
                    **Original Message: **{spoilered_message}
                    
                    Please refrain from using any harmful content to avoid being punished. Please refer to our {rule_channel_obj} for more information. 
                    """,
                    color=embed_color
                )
                embed.set_thumbnail(url=message.author.avatar.url),
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text=f"© {guild.name}", icon_url=guild.icon.url)

                await message.delete()
                await message.channel.send(embed=embed)

        # filtered chat is disabled
        else:
            return

    def check_profanity(self, text):
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
