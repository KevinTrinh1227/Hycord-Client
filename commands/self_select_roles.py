import discord
from discord.ext import commands
import discord.ui
import datetime
import json

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
selection_roles_template = data["embed_templates"]["selection_roles"]
button_data = data["embed_templates"]["selection_roles"]["list_of_roles"]
roles = data["embed_templates"]["selection_roles"]["list_of_roles"]

class Roles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.clicked_button_label = None  # Initialize a variable to store the label

        for role in roles:
            # Create option buttons and assign the callback function
            button = discord.ui.Button(label=role["button_label"], style=discord.ButtonStyle.secondary, custom_id=f"{role['role_id']}")
            button.callback = self.button_callback
            self.add_item(button)

    # Callback function for the option buttons
    async def button_callback(self, interaction: discord.Interaction):
        # Store the label of the clicked button in the instance variable
        self.clicked_button_label = interaction.data["custom_id"]
        role = int(self.clicked_button_label)
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
    @commands.hybrid_command(aliases = ["sr", "serverroles"], brief="roles", description="Print menu for self selecting roles.", with_app_command=True)
    async def roles(self, ctx):
        # Replace the footer text with actual values
        footer_text = selection_roles_template["footer_text"].format(
            guild_name=ctx.guild.name
        )
        
        serverIconLink = ctx.guild.icon.url
        embed = discord.Embed(
            title = selection_roles_template["title"],
            description = selection_roles_template["description"],
            color = embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=footer_text, icon_url = serverIconLink)
        await ctx.send(embed = embed, view = Roles())
        
        
async def setup(client):
    client.add_view(Roles())
    await client.add_cog(selfroles(client))