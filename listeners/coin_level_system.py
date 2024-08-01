import discord
from discord.ext import commands
import json
import random
import time  # For tracking message timestamps
import datetime
from discord.ext import commands
import discord.ui

currency_name = "Coins"

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16)  # convert hex color to hexadecimal format
command_prefix = data["general"]["bot_prefix"]

class LevelingCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.load_user_data()
        self.message_cooldown = {}  # To track message timestamps

        with open("config.json", "r") as f:
            config_data = json.load(f)
            self.coin_level_system_enabled = config_data["features"]["coin_level_system"]

    def load_user_data(self):
        try:
            with open("user_data.json", "r") as f:
                self.user_data = json.load(f)
        except FileNotFoundError:
            self.user_data = {}

    def save_user_data(self):
        with open("user_data.json", "w") as f:
            json.dump(self.user_data, f, indent=2)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.coin_level_system_enabled:  # Skip if the module is disabled in config.json
            return
        elif message.author.bot:  # Skip processing if the message author is a bot
            return
        elif message.content.startswith(command_prefix):  # Skip processing if the message starts with a "!"
            return

        self.load_user_data()  # Reload user data from the file

        user_id = str(message.author.id)
        user_data = self.user_data.get(user_id, {"exp": 0, "level": 0, "coins": 0})

        last_message_timestamp = self.message_cooldown.get(user_id, 0)
        current_timestamp = time.time()
        if current_timestamp - last_message_timestamp < 5:
            return

        self.message_cooldown[user_id] = current_timestamp

        user_data["exp"] += random.randint(1, 5) + 0.25
        # print(user_data["exp"])
        user_data["coins"] += random.randint(1, 5)

        if user_data["exp"] >= user_data["level"] * 100:
            user_data["level"] += 1
            await message.channel.send(f"Congratulations {message.author.mention}! You've leveled up to level {user_data['level']}!")

        self.user_data[user_id] = user_data  # Update user data
        self.save_user_data()


    @commands.hybrid_command(aliases=["prof"], brief="profile",description="View your profile stats", with_app_command=True)
    async def profile(self, ctx):
        if not self.coin_level_system_enabled:
            await ctx.send("The coin and level system is disabled.")
            return

        self.load_user_data()  # Reload user data from the file

        user_id = str(ctx.author.id)
        user_data = self.user_data.get(user_id)

        if user_data is None:
            await ctx.send("You don't have any data yet!")
        else:
            embed = discord.Embed(
                title=f"**{ctx.author}'s Profile**",
                description=f"Now displaying {ctx.author.mention}'s server profile statistics. Use `{command_prefix}expleader` or `{command_prefix}coinleader` to view the server leaderboards.",
                color=embed_color
            )
            # embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.add_field(name='Current Level ⭐', value=f"Lvl. {user_data['level']:}", inline=True)
            embed.add_field(name='Experience ✨', value=f"{user_data['exp']:.2f} xp", inline=True)
            embed.add_field(name='Balance 🪙', value=f"{user_data['coins']} {currency_name}", inline=True)
            # Handle user avatar
            if ctx.author.avatar:
                embed.set_thumbnail(url=ctx.author.avatar.url)
            # else:
                # embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
            # await ctx.send(f"Level: {user_data['level']}, Exp: {user_data['exp']}, Coins: {user_data['coins']}")

    @commands.hybrid_command(aliases=["el", "expleaderboard"], brief="expleaderboard",description="Show the top 10 EXP members", with_app_command=True)
    async def expleader(self, ctx):
        if not self.coin_level_system_enabled:
            await ctx.send("The coin and level system is disabled.")
            return

        self.load_user_data()  # Reload user data from the file

        sorted_data = sorted(self.user_data.items(), key=lambda x: x[1]["exp"], reverse=True)
        leaderboard_text = ""
        for idx, (user_id, data) in enumerate(sorted_data[:10], start=1):
            user = self.client.get_user(int(user_id))
            if user:
                leaderboard_text += f"**{idx}. {user.mention} \t Lvl. {data['level']} \t Total Exp: {data['exp']:.2f}**\n"
            else:
                leaderboard_text += f"**{idx}. Unknown User \t Level {data['level']} \t Exp {data['exp']}**\n"
        embed = discord.Embed(
            title=f"**Leaderboards (Experience) ✨**",
            description=f"{leaderboard_text}",
            color=embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url=ctx.guild.icon.url)
        await ctx.send(embed=embed)
        # await ctx.send(leaderboard_text)

    @commands.hybrid_command(aliases=["cl", "coinleaderboard"], brief="coinleader",description="Show the top 10 currency members", with_app_command=True)
    async def coinleader(self, ctx):
        if not self.coin_level_system_enabled:
            await ctx.send("The coin and level system is disabled.")
            return

        self.load_user_data()  # Reload user data from the file

        sorted_data = sorted(self.user_data.items(), key=lambda x: x[1]["coins"], reverse=True)
        leaderboard_text = ""
        for idx, (user_id, data) in enumerate(sorted_data[:10], start=1):
            user = self.client.get_user(int(user_id))
            if user:
                leaderboard_text += f"**{idx}. {user.mention} \t {data['coins']} {currency_name}**\n"
            else:
                leaderboard_text += f"**{idx}. Unknown User \t {data['coins']} {currency_name}**\n"
        embed = discord.Embed(
            title=f"**Leaderboards ({currency_name}) 🪙**",
            description=f"{leaderboard_text}",
            color=embed_color
        )
        embed.timestamp = datetime.datetime.now()
        # embed.set_thumbnail(url="{}".format(ctx.author.avatar.url))
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url=ctx.guild.icon.url)
        await ctx.send(embed=embed)
        # await ctx.send(leaderboard_text)


async def setup(client):
    await client.add_cog(LevelingCog(client))