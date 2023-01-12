import discord
from discord.ext import commands
import json

class MinecraftDisplayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open("linked_accounts.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open("linked_accounts.json", "w") as f:
                json.dump({}, f)

    @commands.command()
    async def mcname(self, ctx):
        """Displays the linked Minecraft account's name"""
        user_id = str(ctx.author.id)
        if user_id in self.data:
            mc_username = self.data[user_id]["mc_username"]
            classification_role_id = self.data[user_id]["classification_role_id"]
            await ctx.send(f"Your linked Minecraft account is: {mc_username} and classification role id is {classification_role_id}.")
        else:
            await ctx.send("Your Discord account is not linked to a Minecraft account.")
            
async def setup(client):
    await client.add_cog(MinecraftDisplayCog(client))