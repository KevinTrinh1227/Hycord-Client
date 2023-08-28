import discord
from discord.ext import commands
import json
import random


class CoinflipCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)  # 5-second cooldown per user
    async def coinflip(self, ctx, choice: str, bet: int):
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

        coin_result = random.choice(coin_choices)

        if choice.lower() == coin_result:
            user_data[user_id]['coins'] += bet * 2  # Win double the bet amount
            result_message = f"Congratulations! You won {bet} coins.\nYour balance before the bet: {balance_before_bet} coins\nYour new balance: {user_data[user_id]['coins']} coins."
        else:
            user_data[user_id]['coins'] -= bet
            result_message = f"Sorry, you lost {bet} coins.\nYour balance before the bet: {balance_before_bet} coins\nYour new balance: {user_data[user_id]['coins']} coins."

        # Update user data in the JSON file
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f, indent=2)

        await ctx.send(result_message)

async def setup(client):
    await client.add_cog(CoinflipCog(client))