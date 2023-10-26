import discord
from discord.ext import commands
import discord.ui
import datetime
import json
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)
    
# Load the "join_dm_message" template
join_dm_template = data["embed_templates"]["join_dm_message"]
    
#json data to run bot
bot_prefix = data["general"]["bot_prefix"]
embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
leave_channel_id = int(data["text_channel_ids"]["bot_logs"])    # logs the bot logs in this channel
member_role_id = int(data["role_ids"]["unverified_member"])
welcome_channel_id = int(data["text_channel_ids"]["welcome"])
pre_embed_color = data["general"]["embed_color"].strip("#")

font_title = ImageFont.truetype("./assets/fonts/Minecraft.ttf", 20)
font_footer = ImageFont.truetype("./assets/fonts/Minecraft.ttf", 15)


class joinleave(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        
    #on member join event        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        def hex_to_rgb(hex_color):
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        member_count = len(member.guild.members) # total guild members
        
        # Load the background image
        background_image = Image.open("./assets/backgrounds/welcome_banner.png")

        if member.avatar:
            pfp_url = member.avatar.url
        else:
            pfp_url = member.guild.icon.url

        pfp_response = requests.get(pfp_url)
        member_pfp = Image.open(BytesIO(pfp_response.content))
        member_pfp = member_pfp.resize((100, 100))

        # Calculate the center coordinates of the background image
        image_width, image_height = background_image.size
        center_x = image_width // 2
        center_y = image_height // 2

        # Calculate the position to paste the circular profile picture at the center
        paste_x = center_x - member_pfp.width // 2
        paste_y = center_y - member_pfp.height // 2

        # Create a circular mask for the profile picture (based on its size)
        mask = Image.new('L', (member_pfp.width, member_pfp.height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, member_pfp.width, member_pfp.height), fill=255)
        member_pfp.putalpha(mask)
        
        
        """
        # Create a colored circle
        circle_radius = 42  # Adjust the radius as needed
        circle_color = hex_to_rgb(pre_embed_color)  # Specify your desired circle color (red in this example)
        draw = ImageDraw.Draw(background_image)
        draw.ellipse((center_x - circle_radius, center_y - circle_radius, center_x + circle_radius, center_y + circle_radius), fill=circle_color)
        """
        

        # Paste the circular profile picture at the center
        background_image.paste(member_pfp, (paste_x, paste_y), member_pfp)

        # Calculate the center x-coordinate for text
        image_width, _ = background_image.size
        text1 = f"{member} has joined! (#{member_count})"
        text2 = f"Welcome to {member.guild.name}, and enjoy your stay!"

        draw = ImageDraw.Draw(background_image)

        _, _, text1_width, _ = draw.textbbox((0, 0), text1, font=font_title)
        _, _, text2_width, _ = draw.textbbox((0, 0), text2, font=font_footer)

        center_x1 = (image_width - text1_width) // 2
        center_x2 = (image_width - text2_width) // 2

        draw = ImageDraw.Draw(background_image)
        draw.text((center_x1, 10), text1, (255, 255, 255), font=font_title)
        draw.text((center_x2, 165), text2, (255, 255, 255), font=font_footer)

        background_image.save("./assets/outputs/welcome.png")  # Save the image

        
        #Auto role feature
        role = member.guild.get_role(member_role_id) #ID of normal member role
        roleStr = str(role)
        autoRole = discord.utils.get(member.guild.roles, name = roleStr)
        
        
        #welcome embed
        channel = self.client.get_channel(welcome_channel_id)
        
        """
        embed = discord.Embed(
            title=(f"Welcome to {member.guild.name}, {member} (#{member_count})"),
            description = f\"""
            Welcome to the {member.guild.name}! Verify your account using `/verify [your IGN]`.

            *THIS IS A PLACEHOLDER WELCOME MESSAGE
            YOU CAN EDIT THIS IN "~/Hycord-Bot/listeners/member_join_leave.py"*

            Member: {member.mention} 
            \""",
            colour= embed_color
            )
        embed.timestamp = datetime.datetime.now()
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        else:
            embed.set_thumbnail(url=member.guild.icon.url)
        #embed.set_image(url="https://imgur.com/btR7AnN.png")
        embed.set_footer(text=f"©️ {member.guild.name}", icon_url = member.guild.icon.url)
        """
        file = discord.File("./assets/outputs/welcome.png")
        embed = discord.Embed(
            description = f"Welcome to {member.guild.name}, {member.mention}!",
            colour= embed_color
            )
        embed.set_image(url="attachment://welcome.png")
        
        # Replace placeholders with actual values
        title = join_dm_template["title"].format(
            guild_name=member.guild.name,
            member=member,
            member_count=member_count
        )

        description = join_dm_template["description"].format(
            guild_name=member.guild.name,
            member_mention=member.mention,
            member_name = member.name
        )

        footer_text = join_dm_template["footer_text"].format(
            guild_name=member.guild.name
        )
        
        embed2 = discord.Embed(
            title=title,
            description =description,
            colour= embed_color
            )
        embed2.timestamp = datetime.datetime.now()
        embed2.set_footer(text=footer_text, icon_url = member.guild.icon.url)
        
        try:
            await member.send(embed=embed2)     # sends the custom dm embed to user
        except:
            pass                                # means user has DMS off
        
        
        await channel.send(f"||{member.mention}||")
        await channel.purge(limit = 1)
        await channel.send(file = file, embed=embed)
        await member.add_roles(autoRole)
    

    # on member leave event
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        
        channel = self.client.get_channel(leave_channel_id)
        embed = discord.Embed(
            title=(f"{member.display_name} has left the server."),
            description=f"{member.mention} has left {member.guild.name}.",
            colour= embed_color
            )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"©️ {member.guild.name}", icon_url = member.guild.icon.url)
        await channel.send(embed=embed)

        
async def setup(client):
    await client.add_cog(joinleave(client))
    
    

