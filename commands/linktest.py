import discord
from discord.ext import commands
import json

class MinecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        try:
            with open("verified_accounts.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open("verified_accounts.json", "w") as f:
                json.dump({}, f)

    async def save_data(self):
        with open("verified_accounts.json", "w") as f:
            json.dump(self.data, f)

    @commands.command()
    async def linkmc(self, ctx, mc_username: str, classification_role_id: int):
        """Links the user's Discord account to a Minecraft account"""
        user_id = str(ctx.author.id)
        if user_id in self.data:
            return await ctx.send("You have already linked your account.")
        self.data[user_id] = {
            "mc_username":mc_username, 
            "classification_role_id":classification_role_id
            }
        await ctx.send(f'Linked Minecraft account {mc_username} to Discord account {ctx.author.name} with classification role id {classification_role_id}.')
        await self.save_data()

        
async def setup(client):
    await client.add_cog(MinecraftCog(client))