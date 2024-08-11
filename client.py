import discord
from discord.ext import commands
import discord.ui
import os
from dotenv import load_dotenv
import json
from discord import app_commands


""" ==========================================
* CONFIG.JSON SECTION
*
* This block creates a config.json for
* an initial bot setup with the following
* default values.
========================================== """

if not os.path.exists('config.json'):
    default_config = {
        "config": {
            "bool": 0
        },
        "general": {
            "bot_prefix": "!",
            "embed_color": "#FF0000",
            "discord_server_guild_id": ""
        },
        "features": {
            "filtered_chat": 0,
            "inactivity_cmd": 0,
            "punishments_cmd": 0
        },
        "category_ids": {
            "tickets_category": ""
        },
        "voice_channel_ids": {
            "member_count": "",
            "members_online": "",
            "guild_member_online": ""
        },
        "text_channel_ids": {
            "welcome": "",
            "inactivity_notice": "",
            "guild_news": "",
            "tickets_transcripts": "",
            "daily_guild_points": "",
            "bot_logs": ""
        },
        "role_ids": {
            "guild_member": "",
            "verified_member": "",
            "unverified_member": "",
            "staff_member": "",
        },
        "hypixel_ids": {
            "guild_id": ""
        },
        "embed_templates": {
            "verification_nickname": {
            "verified_non_guild_member": "[v] {ign}",
            "verified_guild_member": "{guild_rank} | {ign} ✔"
            },
            "welcome_embed": {
            "embed_description": "Welcome to {guild_name}, {member.mention}!",
            "photo_title": "{member.name} has joined! (#{member_count})",
            "photo_footer": "Welcome to {guild.name}, and enjoy your stay!"
            },
            "join_dm_message": {
            "title": "Welcome to {guild_name}, {member} (#{member_count})",
            "description": "Welcome to the {guild_name}! Verify your account using `/verify [Hypixel Username]`.\n\nMember: {member_mention}\n\nPlease be sure to read our server rules and if you have any questions, contact a staff member. Enjoy your stay!",
            "footer_text": "\u00a9\ufe0f {guild_name}"
            },
            "server_rules": {
            "title": "**🔖 | DISCORD SERVER RULES**",
            "description": "(+) Be respectful and kind to all members.\n(+) No spamming or excessive advertising.\n(+) Use appropriate and safe-for-work content.\n(+) No discrimination or offensive language.\n(+) Respect privacy and don't share personal information without consent.\n(+) Stay on-topic and avoid derailing discussions.\n(+) Follow Discord's terms of service and guidelines.\n(+) No trolling, baiting, or disruptive behavior.\n(+) Respect server staff and their instructions.\n(+) Report issues to server staff.\n(+) No excessive self-promotion or spamming personal links.\n(+) Keep discussions civil and avoid arguments.",
            "footer_text": "\u00a9\ufe0f {guild_name}"
            },
            "information": {
            "title": "**📌 | Server Information**",
            "description": "Welcome to the Community discord server. Be sure to view all of our rules and select our self-roles. Please do not abuse any server bots and members. In order to use our bot please use `/help` to view the bot's commands menu.\n\n**Bot Help Command:** `/help`\n\nFor additional help or information please contact a staff member. Enjoy your stay!",
            "footer_text": "\u00a9\ufe0f {guild_name}"
            },
            "selection_roles": {
            "title": "**🔔 | PUBLIC SELF SELECTION ROLES**",
            "description": "Use the following buttons below to chose your own personal roles. By clicking the button, you will claim or unclaim the specified role.",
            "footer_text": "\u00a9\ufe0f {guild_name}",
            "list_of_roles": [
                { "button_label": "🛏️ Bedwars", "role_id": 1166655627708342352 },
                { "button_label": "🗡️ Duels", "role_id": 1166655663162802207 },
                { "button_label": "⚔️ Skywars", "role_id": 1166655647459315743 },
                { "button_label": "🕹️ Arcade", "role_id": 1166855643995590757 }
            ]
            },
            "ticket_system": {
            "title": "**🎟️ | Ticket Support**",
            "description": "Require Support? Click a button below with the corresponding category's emoji and a private channel will be created where our staff team will be ready to assist you!\n\n**Categories**\n🔨 Report a cheater\n🫂 Apply for staff\n📮 Request a role(s)\n🔥 Apply for guild\n🔍 Other\n\nPlease be patient with our team & any ticket abuse will result in a punishment. Note: only 1 ticket can be opened at a time.",
            "footer_text": "\u00a9\ufe0f {guild_name}",
            "ticket_type_list": [
                {
                "button_label": "Report a cheater",
                "ticket_type": "🔨 | Report a cheater",
                "ticket_type_emoji": "🔨"
                },
                {
                "button_label": "Apply for staff",
                "ticket_type": "🫂 | Apply for staff",
                "ticket_type_emoji": "🫂"
                },
                {
                "button_label": "Request a role(s)",
                "ticket_type": "📮 | Request a role(s)",
                "ticket_type_emoji": "📮"
                },
                {
                "button_label": "Apply for guild",
                "ticket_type": "🔥 | Apply for guild",
                "ticket_type_emoji": "🔥"
                },
                {
                "button_label": "Other",
                "ticket_type": "🔍 | Other",
                "ticket_type_emoji": "🔍"
                }
            ]
            }
        }
    }

    with open('config.json', 'w') as config_file:
        json.dump(default_config, config_file, indent=2)
        
        
errors = []


def activateBot (discord_bot_token, bot_prefix, discord_application_id):
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix = bot_prefix, case_insensitive=True, intents=intents, application_id = discord_application_id)
    client.remove_command("help") #removes the default help command
            

    # If the bot is already configured meaning that inside the config.json
    # ["config"]["bool"] == 1, then we run as normal.


    """ ==========================================
    * BOT START UP SECTION
    *
    * This block starts up the bot. Here it 
    * checks if the config.json has already been
    * configured. If it hasnt, then it only loads
    * loads up the listeners.command_errors, and
    * commands.setup cog.
    ========================================== """
    @client.event
    async def on_ready():
        
        print("""
   __ __                     __           __ 
  / // /_ _________  _______/ / ___  ___ / /_
 / _  / // / __/ _ \/ __/ _  / / _ \/ -_) __/
/_//_/\_, /\__/\___/_/  \_,_(_)_//_/\__/\__/ 
    /___/                                   """)
        
        # Open the JSON file and read in the data
        with open('config.json') as json_file:
            data = json.load(json_file)
        
        name = client.user.name.upper()
        discriminator = client.user.discriminator.upper()
        print("--------------------------------------------------")
        print(f"* LOGGED IN AS: {name}#{discriminator}")
        
        if data["config"]["bool"] == 0:
            await client.load_extension("listeners.command_errors")
            await client.load_extension('commands.setup')
            await client.load_extension('commands.restart_client')
            await client.tree.sync()
            print("YOUR BOT REQUIRES AN INITIAL SETUP. 🟡")
            print("--------------------------------------------------")
            for x in range(0, 10):
                print("* USE: \"/setup\" or \"!setup\" IN YOUR SERVER TO BEGIN.")
            print("--------------------------------------------------")
                
        else:
            print("--------------------------------------------------")
            await load_cogs()
            print(f"* {os.path.splitext(os.path.basename(__file__))[0]:<30}{'Successful':<12}🟢")

            # Sync the commands to Discord.
            await client.tree.sync()

            print("--------------------------------------------------")
            await print_errors()
            #change_stats_channels.start()
            

    async def load_cogs():
        # Load in all listeners
        print(f"{'LISTENER FILES':<30}  {'LOAD STATUS':<30}")
        for filename in os.listdir("./listeners"):
            if filename.endswith(".py"):
                try:
                    await client.load_extension(f"listeners.{filename[:-3]}")
                    print(f"* {os.path.splitext(filename)[0]:<30}{'Successful':<12}🟢")
                except Exception as e:
                    errors.append(e)
                    print(f"* {os.path.splitext(filename)[0]:<30}{'Failed':<12}🔴")
        print(f"\n{'COMMAND FILES':<30}  {'LOAD STATUS':<30}")
        # Load in all commands
        for filename in os.listdir("./commands"):
            if filename.endswith(".py"):
                try:
                    await client.load_extension(f"commands.{filename[:-3]}")
                    print(f"* {os.path.splitext(filename)[0]:<30}{'Successful':<12}🟢")
                except Exception as e:
                    errors.append(e)
                    print(f"* {os.path.splitext(filename)[0]:<30}{'Failed':<12}🔴")
        print(f"\n{'OTHER FILES':<30}  {'LOAD STATUS':<30}")
        

    async def print_errors():
        if len(errors) != 0:
            print("ERRORS occured during startup:")
            for error in errors:
                print(error)
        else:
            pass
            
            
    client.run(discord_bot_token)
        