import discord
from discord.ext import commands
import json
import random
import datetime

currency_name = "coins"
chance_of_winning = 0.45        # 0.67 means 67% of winning
cool_down_time = 5              # 5 means 5 seconds of cooldown

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16)  # convert hex color to hexadecimal format

class CoinflipCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(aliases=["cf"], brief="cf [bet amount] [heads/tails]",description="Gamble using coinflip", with_app_command=True)
    @commands.cooldown(1, cool_down_time, commands.BucketType.user)  # 5-second cooldown per user
    async def coinflip(self, ctx: commands.Context, bet: int, choice: str):
        # Load user data from the JSON file
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)

        # Load configuration data from the config.json file
        with open('config.json', 'r') as config_file:
            config_data = json.load(config_file)

        # Check if the coin and level system feature is enabled
        coin_level_system_enabled = config_data.get("features", {}).get("coin_level_system", 0)

        if not coin_level_system_enabled:
            await ctx.send("The coin and level system is disabled.")
            return

        # Get user's ID
        user_id = str(ctx.author.id)

        if user_id not in user_data:
            await ctx.send("You don't have an account yet.")
            return

        user_balance = user_data[user_id]['coins']

        if bet <= 0:
            await ctx.send("Please bet a positive amount.")
            return

        if bet > user_balance:
            await ctx.send("You don't have enough funds to place that bet.")
            return

        coin_choices = ['heads', 'tails']

        if choice.lower() not in coin_choices:
            await ctx.send("Please choose either 'heads' or 'tails' for your coin flip.")
            return

        balance_before_bet = user_balance  # Store the user's balance before the bet

        if choice.lower() == "heads":
            opposite_choice = "tails"
        else:
            opposite_choice = "heads"

        random_number = random.random()

        if (choice.lower() == "heads" and random_number < 0.3) or (choice.lower() == "tails" and random_number < 0.3):
            user_data[user_id]['coins'] += bet * 2  # Win double the bet amount
            # result_message = f"Congratulations! You won {bet} coins.\nYour balance before the bet: {balance_before_bet} coins\nYour new balance: {user_data[user_id]['coins']} coins."
            embed = discord.Embed(
                title=f"**🏆 | CONGRATULATIONS YOU WON!**",
                description=f"{ctx.author.mention} bet `{bet}` {currency_name} and won `{bet * 2}` {currency_name}. You guessed {choice.lower()} and the coinflip landed on {choice.lower()}! You can try again in {cool_down_time} second(s).",
                color=embed_color
            )
            # embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.add_field(name='Before Balance', value=f"{balance_before_bet}", inline=True)
            embed.add_field(name='Net Profit', value=f"{bet:.2f}", inline=True)
            embed.add_field(name='Current Balance', value=f"{user_data[user_id]['coins']} {currency_name}", inline=True)
            embed.set_thumbnail(url="{}".format(ctx.author.avatar.url))
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
        else:
            user_data[user_id]['coins'] -= bet
            # result_message = f"Sorry, you lost {bet} coins.\nYour balance before the bet: {balance_before_bet} coins\nYour new balance: {user_data[user_id]['coins']} coins."
            embed = discord.Embed(
                title=f"**☹️ | SORRY, YOU LOST!**",
                description=f"{ctx.author.mention} bet `{bet}` {currency_name} and lost. You chose {choice.lower()} and the coinflip landed on {opposite_choice}. You can try again in {cool_down_time} second(s).",
                color=embed_color
            )
            # embed.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.add_field(name='Before Balance', value=f"{balance_before_bet}", inline=True)
            embed.add_field(name='Loss Amount', value=f"{bet:.2f}", inline=True)
            embed.add_field(name='Current Balance', value=f"{user_data[user_id]['coins']}", inline=True)
            embed.set_thumbnail(url="{}".format(ctx.author.avatar.url))
            embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url=ctx.guild.icon.url)
            await ctx.send(embed=embed)

        # Update user data in the JSON file
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f, indent=2)

        # await ctx.send(result_message)

async def setup(client):
    await client.add_cog(CoinflipCog(client))