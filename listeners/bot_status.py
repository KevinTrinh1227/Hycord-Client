import discord
from discord.ext import commands
from discord.ext import tasks
import discord.ui
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

command_prefix = data["general"]["bot_prefix"]
# global variable to switch statuses
x = 0


class bot_status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.bot_status.start()

    @tasks.loop(seconds=2)
    async def bot_status(self):
        global x
        if (x <= 60):
            sweaty_role = discord.utils.get(self.client.guilds[0].roles, id=int(data["role_ids"]["guild_member"]))
            online_and_sweaty_members = len([member for member in self.client.guilds[0].members if
                                             sweaty_role in member.roles and member.status != discord.Status.offline])
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                        name=f"{online_and_sweaty_members} Guild Members"))
            x += 1
        elif (61 <= x <= 120):
            x += 1
            await self.client.change_presence(activity=discord.Game(name="with sweats 🔪"))
        elif (121 <= x <= 180):
            x += 1
            await self.client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name=f"{command_prefix}help command 🔎"))
        else:
            x = 0


async def setup(client):
    await client.add_cog(bot_status(client))
