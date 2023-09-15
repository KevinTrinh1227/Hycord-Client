<h1 align="center">
  <a href="https://www.hycord.netlify.app" target="_blank"><img src="https://user-images.githubusercontent.com/48145892/218457340-39c08f69-e027-4529-b907-b2414435af77.png">
</h1>
<p align="center">
  An all-in-one Minecraft Hypixel stats and moderation bot.
</p>
<p align="center">
  Visit the <a href="https://hycord.netlify.app" target="_blank"><strong>Hycord Project Page</strong></a> for more information.
</p>

[![808afada7b715665ba13571e12d93d12](https://user-images.githubusercontent.com/48145892/221743994-65274a3b-601b-4193-9b41-4e0851ca8578.gif)](https://hycord.netlify.app)

## Bot Features

| Bot Feature | Command Usage | Aliasses    | Description                  |
| :----------: | :---------:| :---------:| :--------------------------:|
| Link Account  | `!verify [Hypixel username]` | `link` `sync`  | Validates and syncs your Discord account to your Hypixel account  |
| Update Account  | `!update` | `N/A`  | Update your account info in the server. (Useful if your level went up or you changed your Hypixel username)  |
| Display Guild Points    | `!guildpoints` | `dp` `dgp`   | Display current daily guild points from each guild member    |
| Auto Gexp Announcement    | `N/A` | `N/A`   | Sends an embed message of all guild points earned by every member in a specified channel     |
| Bedwars Statistics    | `!bwstats [Hypixel username]` | `bws` `bwstat`   | View a certain Hypixel player's in-game Bedwars statistics    |
| Inactivity    | `!inactive` | `mia`  | Send a custom Hypixel guild inactivity notice embed message to a specified channel     |
| Ticket System  | `!tickets` | `t`  | Sends a ticket menu message with buttons that allow users to create their own support tickets  |
| Announcements    | `!announce` | `announcement` `a`   | Create a custom embed message and send it to any channel    |
| Say    | `!say [Message]` | `yell` `s`   | Send any message as an embed to current channel    |
| Avatar    | `!avatar [@mention member]` | `pfp` `av`   | Get a certain user's avatar profile picture    |
| Bedwars Statistics    | `!bwstats [Hypixel username]` | `bws` `bwstat`   | View a certain Hypixel player's in-game Bedwars statistics    |
| Guild List    | `!guildlist` | `gl`  | Show a list of all current members within the Hypixel guild    |
| Help Command    | `!help` | `idk` `h` `aid`  | Show all bot commands, aliases, and command usage examples    |
| Custom Welcome Message    | `N/A` | `N/A`   | Sends a customizable welcome message in a specified channel     |
| Cycling Bot Status    | `N/A` | `N/A`   | Rotating bot statuses with placeholders inside     |
| Server Information    | `!information` | `info` `inform`  | Print out a custom information embed message for your server   |
| Ping    | `!ping` | `lt`  | View your bot's current latency connection speed    |
| Ban Player   | `!ban [@mention member]` | `b`  | Ban a player from your server. This punishment will also be logged in a specified channel  |
| Kick Player   | `!kick @[mention member]` | `k`  | Kick a player from your server. This punishment will also be logged in a specified channel  |
| Purge Messages   | `!purge [integer value]` | `clear` `del`  | Clear a specified amount of message in that specific channel  |
| Rules   | `!rules` | `r` `rule`  | Display the discord server rules in a customizable embed message  |
| Role Claiming  | `!roles` | `sr`  | Sends a customizable public roles menu with buttons to select desired roles  |
| Unlink Account | `!unverify` | `unlink`  | Unlinks your discord account from your in-game Hypixel account  |
| User Info  | `!whois @[mention member]` | `who`  | Displays general information about a certain discord user  |
| Verification Stats  | `!vstats` | `vs`  | Sends your server's verified users report  |
<p align="center">
  NOTE: The Hycord setup video may be outdated. Please refer to the guide below for an accurate up-to-date setup guide. 
</p>


## Getting Started

### 📋 Clone the Repository
1) Open the desired directory in the command prompt
2) Clone the repository using the command below

    ```sh
    git clone https://github.com/KevinTrinh1227/Hycord-Bot.git
    ```

### 🛠 set-up
1. Obtain a <a href="https://www.writebots.com/discord-bot-token/" target="_blank">Discord bot token</a> and <a href="https://developer.hypixel.net/" target="_blank">Hypixel API key</a>
   ```sh
   Administrator bot permissions is recommended to avoid any issues. 
   ```
   ```sh
   Enable the "Public Bot" module AND all Privileged Gateway Intents (3 total)
   Discord Dev > Applications > [Your App] >  Bot > "Privileged Gateway Intents"
   ```
2. Create a "`.env`" file with your tokens and API keys

   ```sh
   DISCORD_BOT_TOKEN=<YOUR_DISCORD_BOT_TOKEN>
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

2. Setup the initial bot setup and enjoy

   ```sh
   !setup
   ```