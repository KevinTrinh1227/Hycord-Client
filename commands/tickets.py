import discord
from discord.ext import commands
import discord.ui
import datetime
import json
import asyncio
import io
import chat_exporter

# Open the JSON file and read in the data
with open('config.json') as json_file:
    data = json.load(json_file)

embed_color = int(data["general"]["embed_color"].strip("#"), 16) #convert hex color to hexadecimal format
bot_prefix = data["general"]["bot_prefix"]

category_id = int(data["category_ids"]["tickets_category"])
staff_role_id = int(data["role_ids"]["staff_member"])
transcript_channel_id = int(data["text_channel_ids"]["tickets_transcripts"])
bot_logs = int(data["text_channel_ids"]["bot_logs"])

ticket_types = data["embed_templates"]["ticket_system"]["ticket_type_list"]

class Roles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.clicked_button_label = None  # Initialize a variable to store the label

        for ticket_type in ticket_types:
            # Create option buttons and assign the callback function
            button = discord.ui.Button(label=ticket_type["button_label"], style=discord.ButtonStyle.secondary, custom_id=ticket_type['ticket_type'], emoji=ticket_type['ticket_type_emoji'])
            button.callback = self.button_callback
            self.add_item(button)

    # Callback function for the option buttons
    async def button_callback(self, interaction: discord.Interaction):
        
        guild = interaction.guild
        category = guild.get_channel(category_id)
        staff_role = guild.get_role(staff_role_id)
        user = interaction.user
        ticket_type = interaction.data["custom_id"]
        #print(ticket_type)
        
        for ticket in ticket_types:
            #print("Comparing", ticket_type, "to", ticket)
            if ticket_type == ticket["ticket_type"]:
                emoji = ticket["ticket_type_emoji"]
                #print(type(emoji), emoji)
        
        # Checks if user already has a ticket open
        for channel in category.channels:
            # print(channel.name)
            channel_name_cleaned = channel.name[7:-2]
            if channel_name_cleaned == user.name:
                # User already has an open ticket
                # print(f"{user.name} already has a ticket open. {channel.id}")
                try:
                    # Attempt to send a private message to the user
                    embed = discord.Embed(
                        title=f"**🎟️ | You already have an open ticket**",
                        description=f"""
                        Note that you can only have 1 ticket open at a time. To access your current ticket, click the channel reference below.
                        
                        **Your ticket ➜** <#{channel.id}>
                        
                        Remember that any abuse of our ticket system could result in a punishment. Please be patient with our staff team.
                        """,
                        color=embed_color
                    )
                    embed.timestamp = datetime.datetime.now()
                    #embed.set_thumbnail(url="{}".format(guild.icon.url)),
                    embed.set_footer(text=f"©️ {guild.name}", icon_url=guild.icon.url)
                    
                    log_embed = discord.Embed(
                        title=(f"🎟️ | {user.name} tried opening another ticket - [Warn Message Sent]"),
                        description=f"{user.mention} tried to open another ticket but they already have one opened. A warning message has been sent to them.",
                        colour= embed_color
                        )
                    log_embed.timestamp = datetime.datetime.now()
                    log_embed.set_footer(text=f"©️ {guild.name}", icon_url=guild.icon.url)
                    
                    await user.send(embed=embed)
                    await guild.get_channel(bot_logs).send(embed=log_embed)
                    
                except:
                    # If user DMs are off
                    log_embed = discord.Embed(
                        title=(f"🎟️ | {user.name} tried opening another ticket - [No Warn Message]"),
                        description=f"{user.mention} tried to open another ticket but they already have one opened. A warning message could **not** be sent because they have DMs set to private.",
                        colour= embed_color
                        )
                    log_embed.timestamp = datetime.datetime.now()
                    log_embed.set_footer(text=f"©️ {guild.name}", icon_url=guild.icon.url)
                    
                    await guild.get_channel(bot_logs).send(embed=log_embed)
                    await interaction.response.defer()
                    
                return
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await category.create_text_channel(f'ticket-{user.name}-{emoji}', overwrites=overwrites)
        
        self.clicked_button_label = interaction.data["custom_id"]
        ticket_type = interaction.data["custom_id"]
        
        role_id = staff_role_id #staff member role ID
        staff_role = guild.get_role(role_id)
        await channel.send(f"||{staff_role.mention}{user.mention}||")
        await channel.purge(limit = 1)
        
        embed = discord.Embed(
            title = f"**{ticket_type} Ticket**",
            description = f"Please describe your issue clearly and a staff member will assist you shortly. Be sure to provide any attachments if necessary.\n\nTicket Issuer: {user.mention}\n\nUse the command `{bot_prefix}close` to close this ticket.",
            color = embed_color
        )
        embed.set_author(name=f"Requested by {user}", icon_url=user.avatar.url),
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url="{}".format(guild.icon.url)),
        embed.set_footer(text=f"©️ {guild.name}", icon_url = guild.icon.url)
        await channel.send(embed = embed)
        await interaction.response.defer()
 

class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.category_id = category_id  # Replace with your desired category ID
        self.staff_role_id = staff_role_id  # Replace with your staff role ID

    @commands.has_permissions(administrator=True)
    @commands.hybrid_command(aliases=["ticket"], brief="ticket", description="Sends a ticket menu", with_app_command=True)
    async def tickets(self, ctx):
        await ctx.channel.purge(limit=1)
        serverIconLink = ctx.guild.icon.url
        embed = discord.Embed(
            title = f"**{ctx.guild.name} Support**",
            description = """
            Require Support? Click a button below with the corresponding category's emoji and a private channel will be created where our staff team will be ready to assist you!\n\n**Categories**\n🔨 Report a cheater\n🫂 Apply for staff\n📮 Request a role(s)\n🔥 Apply for guild\n🔍 Other\n\nPlease be patient with our team & any ticket abuse will result in a punishment. Note: only 1 ticket can be opened at a time. 
            """,
            color = embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url="{}".format(ctx.guild.icon.url)),
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = serverIconLink)
        await ctx.send(embed = embed, view = Roles())

    @commands.hybrid_command(aliases=["close"], brief="closeticket", description="Closes the current ticket", with_app_command=True)
    async def closeticket(self, ctx):
        if not ctx.channel.name.startswith("ticket-"):
            #await ctx.send("This command can only be used in a ticket channel.")
            pass
            return

        # Create a confirmation message
        embed = discord.Embed(
            title="🎟️ | Confirmation",
            description="Are you sure that you want to close your ticket? If so please click on the reaction below this message. Otherwise please ignore this message.",
            color=embed_color
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
        confirm_msg = await ctx.send(embed=embed)

        # Add a check mark reaction to the message
        await confirm_msg.add_reaction("✅")

        # Wait for the author to react with a check mark
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message == confirm_msg

        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Confirmation timed out. Ticket will not be closed. Run the command again to close.")
            return

            
        #saving the channel as a html
        transcript = await chat_exporter.export(ctx.channel)
        if transcript is None:
            return

        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{ctx.channel.name}.html",
        )

        transcript_channel = self.client.get_channel(transcript_channel_id)
        message = await transcript_channel.send(file=transcript_file)
        link = await chat_exporter.link(message)
        #await ctx.send("Click this link to view the transcript online: " + link)



        # Extract the username from the ticket channel name
        channel_name = ctx.channel.name
        parts = channel_name.split("-")
        username = parts[1]
        # print(f"Channel name: {channel_name}, Username: {username}")
        # Get the user who opened the ticket
        user = discord.utils.get(ctx.guild.members, name=username)
        user_id = user.id if user else None  # Get the user's ID, or None if not found


        #sends this embed message to a staff only chat as a record
        embed3 = discord.Embed(
            title="🎟️ | Ticket Closed",
            url=link,
            description=f"A ticket has been closed, below is a link to the transcript. Ticket issuer ID: {user_id}",
            color=embed_color
        )
        embed3.timestamp = datetime.datetime.now()
        embed3.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
        embed3.add_field(
            name="Ticket Issuer",
            value=f"{username}"
        )
        embed3.add_field(
            name="Closed By",
            value=f"{ctx.author}"
        )
        embed3.add_field(
            name="View transcript",
            value=f"[Click here to view the transcript]({link})"
        )
        
        
        #sends this embed message to the ticket channel
        embed2 = discord.Embed(
            title="🎟️ | Closed | This ticket is now locked",
            url=link,
            description="Your support ticket is now locked. A transcript copy will be sent to you if your DM is set to public. If not, please save the transcript file below.\n\n***This channel will be terminated in 1 minute.\n\n***",
            color=embed_color
        )
        #embed2.set_author(name = f"Closed by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed2.timestamp = datetime.datetime.now()
        embed2.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
        embed2.add_field(
            name="Ticket Issuer",
            value=f"{username}"
        )
        embed2.add_field(
            name="Issuer ID",
            value=f"{user_id}"
        )
        embed2.add_field(
            name="View transcript",
            value=f"[Click here to view the transcript]({link})"
        )


        #sends this embed to the ticket issuer
        embed4 = discord.Embed(
            title=f"🎟️ | {username}\'s Ticket Transcript",
            url=link,
            description=f"A link to your transcript of your ticket has been attached. We encourage that you save the file for future reference. Thank you.",
            color=embed_color
        )
        embed4.timestamp = datetime.datetime.now()
        embed4.set_footer(text=f"©️ {ctx.guild.name}", icon_url = ctx.guild.icon.url)
        embed4.add_field(
            name="Ticket Issuer",
            value=f"{username}"
        )
        embed4.add_field(
            name="Closed By",
            value=f"{ctx.author}"
        )
        embed4.add_field(
            name="View transcript",
            value=f"[Click here to view the transcript]({link})"
        )
        
        
        # to avoid being rate limited, it only affects users without the following roles...
        role_ids = [staff_role_id] #bot role, staff member role
        
        #deleting message above
        await ctx.channel.purge(limit=1)
        
        #sending both embed messages to the channels...
        await ctx.send(embed=embed2)                    # sends the embed to ticket channel
        await transcript_channel.send(embed=embed3)     # sends the embed message to transcripts channel
        if user: 
            # Send the transcript link as a direct message to the user
            try:
                await user.send(embed=embed4)  
                await transcript_channel.send(f"{username} has received a transcript in their DMs. 🟢\nTheir Discord profile ID: `{user_id}`\nTheir Mention: <@{user_id}>")
            except discord.errors.Forbidden:
                # await ctx.send("Unable to send a direct message to the user with the transcript link.")
                await transcript_channel.send(f"{username}'s DMs are private. No transcript sent. 🟡\nTheir Discord profile ID: `{user_id}`\nTheir Mention: <@{user_id}>")



        # Revoke the send messages permission for every user in the channel who doesn't have the specified roles
        for member in ctx.channel.members:
            if not any(role.id in role_ids for role in member.roles):
                await ctx.channel.set_permissions(member, send_messages=False, read_messages=True)

        
        #wait a minute before deleting channel
        await asyncio.sleep(60)  # Wait for 60 seconds before deleting the channel
        await ctx.channel.delete()

async def setup(client):
    client.add_view(Roles())
    await client.add_cog(Ticket(client))