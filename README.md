<h4 align="center">
  <a href="https://www.hycord.net" target="_blank"><img src="https://raw.githubusercontent.com/KevinTrinh1227/Hycord-Bot/main/assets/display_banner.png" alt="Display Banner"></a>
</h4>
<p align="center">
  A versatile Hypixel-integrated Discord.py client.
  Visit <a href="https://hycord.net" target="_blank"><strong>hycord.net</strong></a> for more information.
</p>
<div align="center">
  <img src="https://img.shields.io/badge/maintenance-actively--developed-brightgreen.svg" alt="Maintained status" />
  <img src="https://img.shields.io/github/v/release/KevinTrinh1227/Hycord-Bot.svg" alt="Release badge" />
</div>
<br/>

## 📌 Information

**What is Hycord?** Hycord is a versatile Discord client I've developed, leveraging key features from various public Hypixel and general-purpose bots. From seamless Hypixel integration to robust moderation tools and everything in between, Hycord eliminates the need to clutter your server with numerous bots, ensuring a clean, professional, and fully customizable experience. While originally designed for Hypixel guild communities, Hycord's optional Hypixel integration module allows it to excel as a versatile all-purpose bot, as demonstrated in the accompanying images. This bot streamlines your server setup and enhances the gaming experience.

Should you run into any issues or bugs, please create an [issue ticket](https://github.com/KevinTrinh1227/Hycord-Bot/issues), or if interested, create a [pull request](https://github.com/KevinTrinh1227/Hycord-Bot/pulls). The native development version uses Python 3.10+ and has been tested on Linux and Windows 10+ OS.

## 🛠 Installation & setup

1. Clone the repository OR download the [latest release](https://github.com/KevinTrinh1227/Hycord-Bot/releases)

   ```sh
   git clone https://github.com/KevinTrinh1227/Hycord-Bot.git
   ```

   ```sh
   cd Hycord-Bot
   ```

2. Obtain a <a href="https://www.writebots.com/discord-bot-token/" target="_blank">Discord bot token</a> and <a href="https://developer.hypixel.net/" target="_blank">Hypixel API key</a>

- Administrator bot permissions are recommended to avoid any issues.
- [Applications](https://discord.com/developers/applications) > [Your App] > Bot > "Privileged Gateway Intents"
- Enable all privileged gateway intents (3 total)

3. Create a "`.env`" file with your tokens and API keys

   ```sh
   DISCORD_BOT_TOKEN=<YOUR_DISCORD_BOT_TOKEN>
   DISCORD_APPLICATION_ID=<YOUR_DISCORD_APPLICATION_ID>
   HYPIXEL_API_KEY=<YOUR_HYPIXEL_API_KEY>
   ```

4. Install all dependencies

   ```sh
   pip install -r requirements.txt
   ```

## 🚀 Activate the bot in terminal

1. Build and run the Discord bot

   ```sh
   python main.py
   ```

2. Setup the bot using the cmd in your server

   ```sh
   /setup
   ```

3. Restart your bot after initial setup. Now you're ready to go

   ```sh
   /help
   ```

## Client Features

Note that the lists below may be outdated. Please use `/help` inside your server to view an updated commands menu.
Important: Parameters inside `<>` are required while parameters inside `[]` are optional.

### 🔓 Public Commands (No Permissions)

These commands are open to the public and anyone can execute them.
| Bot Feature | Command Usage | Description |
| :--------------------: | :----------------------------------: |:---------------------------------------------------------------------------------------------------------: |
| Link Account | `/verify <Hypixel username>` | Validates and syncs your Discord account to your Hypixel account |
| Unlink Account | `/unverify` | Unlinks your discord account from your in-game Hypixel account |
| Update Account | `/update` |Update your account info in the server. (Useful if your level went up or you changed your Hypixel username) |
| Guild Information | `/guildinfo` | Displays information about your Hypixel guild |
| Display Guild Points | `/guildpoints` | Display current daily guild points from each guild member |
| Guild List | `/guildlist` | Displays a list of guild members |
| Weekly Points Report | `/weekly <Guild Player Name>` | View a guild member's weekly point contribution |
| Bedwars Statistics | `/bedwars <Player Name>` | View a certain Hypixel player's in-game Bedwars statistics |
| Player Skin | `/skin <Player Name>` | View any Minecraft player's skin. Front and back. |
| Inactivity | `/inactive` | Send a custom Hypixel guild inactivity notice embed message to a specified channel |
| Verification Stats | `/verifiedstats` | Sends your server's verified users report |
| Avatar | `/avatar [@Server Member]` | Get a certain user's avatar profile picture |
| Help Command | `/help [Page Number]` | Show all bot commands, aliases, and command usage examples |
| Server Information | `/information` | Print out a custom information embed message for your server |
| Ping | `/ping` | View your bot's current latency connection speed |
| Rules | `/rules` | Display the discord server rules in a customizable embed message |
| User Info | `/whois [@Server Member]` | Displays general information about a certain discord user |
| Reddit Memes | `/meme` | Displays a random Reddit meme as an embed |
| Experience Leaderboard | `/expleader` | Displays top server members with most XP |
| Coins Leaderboard | `/coinleader` | Displays top server members with most coins |
| Server Profile | `/profile` | Displays your profile information and stats |
| Close Ticket | `/closeticket` | Closes a ticket channel |
| Client Setup | `/setup` | Initial bot setup command. Only works when there is no config file, meaning the bot has not been set up yet. |

### 🔐 Mod Commands (Requires Permissions)

Mod commands require certain permission nodes to execute. View corresponding command files for more info.
| Bot Feature | Command Usage | Description |
| :--------------------: | :----------------------------------: |:---------------------------------------------------------------------------------------------------------: |
| Force Verification | `/forceverify <@Discord Member> <Hypixel username>` | Force sync a discord member to a Hypixel account |
| Force Unverification | `/forceunverify <@Discord Member>` | Force un-sync a discord member from a Hypixel account |
| Ban Player | `/ban [@Server Member]` | Ban a player from your server. This punishment will also be logged in a specified channel |
| Kick Player | `/kick [@Server Member]` | Kick a player from your server. This punishment will also be logged in a specified channel |
| Purge Messages | `/purge <Message Amount>` | Clear a specified amount of message in that specific channel |
| Announcements | `/announce` | Create a custom embed message and send it to any channel |
| Say | `/say <Message>` | Send any message as an embed to current channel |
| Ticket System | `/tickets` | Sends a ticket menu message with buttons that allow users to open their own support tickets |
| Role Claiming | `/roles` | Sends a customizable public roles menu with buttons to select desired roles |

### 🦻 Listeners

These listeners listen for certain event triggers or run asynchronously.
| Bot Feature | Description |
| :-------------------------: | :---------------------------------------------------------------------------------------------------------------------------------: |
| Guild Logs | Sends a message in a specified channel, when a player joins or leaves your Hypixel guild, this also includes if a player was kicked |
| Guild member auto rename | Renames all verified discord guild members to a specific format every specified amount of seconds to ensure they all follow the template in config.json |
| Ticket Transcripts | When tickets are closed, a ticket transcript will be sent to the user who opened the ticket, and a copy will be stored in a specified channel |
| Level & Economy System | Users gain coins and experience points by sending messages and participating in chat |
| Custom Welcome Message | Sends a customizable welcome message in a specified channel |
| Custom Join Private Message | Sends a customizable welcome message in a specified channel |
| General logs | Sends general log reports such as members joining, leaving, editing messages, deleting messages, and more all in a specified channel. |
| Cycling Bot Status | Rotating bot statuses with placeholders inside |
| Auto Gexp Announcement | Sends a message of the top guild point contributors for that specific day in a specified channel |
| Abuse Logs | Sends logs of members abusing tickets system, etc |
| Twitch Integration | Sends a custom message whenever a specified person is streaming on Twitch |
