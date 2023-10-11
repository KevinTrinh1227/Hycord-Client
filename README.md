<h1 align="center">
  <a href="https://www.hycord.net" target="_blank"><img src="https://github.com/KevinTrinh1227/Hycord-Bot/assets/48145892/69bb5241-481e-4e90-bcf0-beed3c968871" width="950px"></a>
</h1>
<p align="center">
  A versatile Hypixel-integrated Discord.py client.
  Visit <a href="https://hycord.net" target="_blank"><strong>hycord.net</strong></a> for more information.
</p>
<div align="center">
  <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" alt="Maintained status" />
  <img src="https://img.shields.io/github/v/release/KevinTrinh1227/Hycord-Bot.svg" alt="Release badge" />
</div>

<h4 align="center">
  <a href="https://www.hycord.net" target="_blank"><img src="https://raw.githubusercontent.com/KevinTrinh1227/Hycord-Bot/main/assets/screenshot_1.png" alt="Screen Shot"></a>
</h4>
<details>
  <summary align="center">VIEW MORE PHOTOS HERE</summary>
    <a href="https://www.hycord.net" target="_blank">
      <img alt="Screen Shot" src="https://raw.githubusercontent.com/KevinTrinh1227/Hycord-Bot/main/assets/screenshot_2.png">
    </a>
</details>

## Getting Started

### 📋 Clone or download the client

1. Clone the repository OR download the [latest release](https://github.com/KevinTrinh1227/Hycord-Bot/releases)

   ```sh
   git clone https://github.com/KevinTrinh1227/Hycord-Bot.git
   ```

   ```sh
   cd Hycord-Bot
   ```

### 🛠 Set-up

1. Obtain a <a href="https://www.writebots.com/discord-bot-token/" target="_blank">Discord bot token</a> and <a href="https://developer.hypixel.net/" target="_blank">Hypixel API key</a>

- Administrator bot permissions are recommended to avoid any issues.
- Enable all privileged gateway intents (3 total)
- [Applications](https://discord.com/developers/applications) > [Your App] > Bot > "Privileged Gateway Intents"

2. Create a "`.env`" file with your tokens and API keys

   ```sh
   DISCORD_BOT_TOKEN=<YOUR_DISCORD_BOT_TOKEN>
   DISCORD_APPLICATION_ID=<YOUR_DISCORD_APPLICATION_ID>
   HYPIXEL_API_KEY=<YOUR_HYPIXEL_API_KEY>
   ```

3. Install all dependencies

   ```sh
   pip install -r requirements.txt
   ```

### 🚀 Activate the bot in terminal

1. Build and run the Discord bot

   ```sh
   python main.py
   ```

2. Setup the bot using the cmd in your server

   ```sh
   /setup
   ```

3. After initial setup, restart your bot/client!
   
   ```sh
   /help
   ```

## Client Features

### 🔓 General Commands

Public commands, no perms required. Note that aliases will not work on slash commands.
| Bot Feature | Command Usage | Aliases | Description |
| :--------------------: | :---------------------------: | :----------------: | :---------------------------------------------------------------------------------------------------------: |
| Link Account | `!verify [Hypixel username]` | `link` `sync` | Validates and syncs your Discord account to your Hypixel account |
| Update Account | `!update` | `N/A` | Update your account info in the server. (Useful if your level went up or you changed your Hypixel username) |
| Display Guild Points | `!guildpoints` | `dp` `dgp` | Display current daily guild points from each guild member |
| Bedwars Statistics | `!bwstats [Hypixel username]` | `bws` `bwstat` | View a certain Hypixel player's in-game Bedwars statistics |
| Inactivity | `!inactive` | `mia` | Send a custom Hypixel guild inactivity notice embed message to a specified channel |
| Avatar | `!avatar [@mention member]` | `pfp` `av` | Get a certain user's avatar profile picture |
| Bedwars Statistics | `!bwstats [Hypixel username]` | `bws` `bwstat` | View a certain Hypixel player's in-game Bedwars statistics |
| Guild List | `!guildlist` | `gl` | Show a list of all current members within the Hypixel guild |
| Help Command | `!help` | `idk` `h` `aid` | Show all bot commands, aliases, and command usage examples |
| Server Information | `!information` | `info` `inform` | Print out a custom information embed message for your server |
| Ping | `!ping` | `lt` | View your bot's current latency connection speed |
| Rules | `!rules` | `r` `rule` | Display the discord server rules in a customizable embed message |
| Unlink Account | `!unverify` | `unlink` | Unlinks your discord account from your in-game Hypixel account |
| User Info | `!whois @[mention member]` | `who` | Displays general information about a certain discord user |
| Verification Stats | `!vstats` | `vs` | Sends your server's verified users report |

### 🔐 Mod Commands (Requires Permissions)

These commands require certain permission nodes to execute. See the corresponding command file for permission node info.
| Bot Feature | Command Usage | Aliases | Description |
| :--------------------: | :---------------------------: | :----------------: | :---------------------------------------------------------------------------------------------------------: |
| Ban Player | `!ban [@mention member]` | `b` | Ban a player from your server. This punishment will also be logged in a specified channel |
| Kick Player | `!kick @[mention member]` | `k` | Kick a player from your server. This punishment will also be logged in a specified channel |
| Purge Messages | `!purge [integer value]` | `clear` `del` | Clear a specified amount of message in that specific channel |
| Announcements | `!announce` | `announcement` `a` | Create a custom embed message and send it to any channel |
| Say | `!say [Message]` | `yell` `s` | Send any message as an embed to current channel |
| Ticket System | `!tickets` | `t` | Sends a ticket menu message with buttons that allow users to create their own support tickets |
| Role Claiming | `!roles` | `sr` | Sends a customizable public roles menu with buttons to select desired roles |

### 🦻 Listeners

These listeners listen for certain event triggers or run asynchronously.
| Bot Feature | Command Usage | Aliases | Description |
| :--------------------: | :---------------------------: | :----------------: | :---------------------------------------------------------------------------------------------------------: |
| Level & Economy System | `N/A` | `N/A` | Users gain coins and exp by sending messages in chat |
| Custom Welcome Message | `N/A` | `N/A` | Sends a customizable welcome message in a specified channel |
| Custom Join Message | `N/A` | `N/A` | Sends a custom private message to a new server member on join |
| Leave Message Logs | `N/A` | `N/A` | Sends a log report for each member that leaves your server in a specified channel |
| Cycling Bot Status | `N/A` | `N/A` | Rotating bot statuses with placeholders inside |
| Auto Gexp Announcement | `N/A` | `N/A` | Sends an embed message of all guild points earned by every member in a specified channel |
