import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format

#reaction roles
class Roles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
    @discord.ui.button(label = "🛏️", custom_id = "Role 1", style = discord.ButtonStyle.secondary)
    async def button1(self, interaction, button):
        role = 934424403150766150
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()
    @discord.ui.button(label = "🗡️", custom_id = "Role 2", style = discord.ButtonStyle.secondary)
    async def button2(self, interaction, button):
        role = 1054991878841446450
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()
    @discord.ui.button(label = "⚔️", custom_id = "Role 9", style = discord.ButtonStyle.secondary)
    async def button9(self, interaction, button):
        role = 1054991871493033994
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()
    @discord.ui.button(label = "🕹️", custom_id = "Role 10", style = discord.ButtonStyle.secondary)
    async def button10(self, interaction, button):
        role = 1054991881420931122
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()
    @discord.ui.button(label = "🔔", custom_id = "Role 7", style = discord.ButtonStyle.secondary)
    async def button7(self, interaction, button):
        role = 934424365020360714
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()
    @discord.ui.button(label = "🫂 ", custom_id = "Role 6", style = discord.ButtonStyle.secondary)
    async def button6(self, interaction, button):
        role = 1054991883937521734
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()
    @discord.ui.button(label = "🎉", custom_id = "Role 5", style = discord.ButtonStyle.secondary)
    async def button5(self, interaction, button):
        role = 1054991875330801744
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()
    @discord.ui.button(label = "🚬", custom_id = "Role 3", style = discord.ButtonStyle.secondary)
    async def button3(self, interaction, button):
        role = 934424330765471764
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()
    @discord.ui.button(label = "📱", custom_id = "Role 4", style = discord.ButtonStyle.secondary)
    async def button4(self, interaction, button):
        role = 934424304379125850
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()
    @discord.ui.button(label = "🍼", custom_id = "Role 8", style = discord.ButtonStyle.secondary)
    async def button8(self, interaction, button):
        role = 934424272758247436
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.defer()
        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.defer()


class selfroles(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.has_permissions(administrator = True)
    @commands.command(aliases = ["sr", "serverroles"], brief="roles", description="Print menu for self selecting roles.")
    async def roles(self, ctx):
        serverIconLink = ctx.guild.icon.url
        embed = discord.Embed(
            title = "**PUBLIC SELF SELECTION ROLES**",
            description = """
            THIS IS A PLACEHOLDER OUTPUT
            TO EDIT THE SELF ROLES GO TO "~/Hycord-Bot/commands/selfroles.py"
            AND EDIT THE ROLE ID'S 

            Use the following menu below to chose your own personal roles. 
            
            <@&934424403150766150>  ➜ Classify as a Bedwars player
            <@&1054991878841446450> ➜ classify as a Skywars player 
            <@&1054991871493033994> ➜ Classify as a Duels Practice player 
            <@&1054991881420931122> ➜ Classify as a Arcade Games player
            
            <@&934424365020360714> ➜ Get pinged for Bedwars parties
            <@&1054991883937521734> ➜ Get pinged for general squads
            <@&1054991875330801744> ➜ Get pinged for community game nights
            <@&934424330765471764> ➜ Classify as age 20+
            <@&934424304379125850> ➜ Classify within age group 17 - 19
            <@&934424272758247436> ➜ Classify within the age group 13 - 16
            
            Click on the corresponding buttons to claim or unclaim a role. Note that roles can always be claimed/unclaimed.""",
            color = embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = serverIconLink)
        await ctx.channel.purge(limit = 1)
        await ctx.send(embed = embed, view = Roles())
        
        
        
async def setup(client):
    client.add_view(Roles())
    await client.add_cog(selfroles(client))