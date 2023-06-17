<h1 align="center">
  <a href="https://www.hycord.netlify.app" target="_blank"><img src="https://user-images.githubusercontent.com/48145892/218457340-39c08f69-e027-4529-b907-b2414435af77.png">
</h1>
<p align="center">
  An all in one fully customizable Discord bot to manage a Hypixel community.
</p>
<p align="center">
  Visit the <a href="https://hycord.netlify.app" target="_blank"><strong>Hycord Project Page</strong></a> for more information.
</p>

[![808afada7b715665ba13571e12d93d12](https://user-images.githubusercontent.com/48145892/221743994-65274a3b-601b-4193-9b41-4e0851ca8578.gif)](https://kevintrinh.dev)

## Bot Features

| Bot Feature | Command Usage | Aliasses    | Description                  |
| :----------: | :---------:| :---------:| :--------------------------:|
| Link Account  | `!verify [Hypixel username]` | `link` `sync`  | Validates and syncs your Discord account to your Hypixel account  |
| Update Account  | `!update` | `N/A`  | Update your account info in the server. (Useful if your level went up or you changed your IGN)  |
| Auto Gexp Announcement    | `N/A` | `N/A`   | Sends an embed message of all guild points earned by every member in a specified channel     |
| Ticket System  | `!tickets` | `t`  | Sends a ticket menu message with buttons that allows users to create their own support tickets  |
| Display Guild Points    | `!guildpoints` | `dp` `dgp`   | Display current daily guild points from each guild member    |
| Announcements    | `!announce` | `announcement` `a`   | Create a custom embed message and send it to any channel    |
| Say    | `!say [Message]` | `yell` `s`   | Send any message as an embed to current channel    |
| Avatar    | `!avatar [@mention member]` | `pfp` `av`   | Get a certain user's avatar profile picture    |
| Bedwars Statistics    | `!bwstats [Hypixel username]` | `bws` `bwstat`   | View a certain Hypixel player's in-game bedwars statistics    |
| Guild List    | `!guildlist` | `gl`  | Show a list of all current members within the Hypixel guild    |
| Help Command    | `!help` | `idk` `h` `aid`  | Show all bot commands, aliases, and command usage examples    |
| Inactivity    | `!inactive` | `mia`  | Send a custom inactivity notice embed message to a specified channel     |
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


## Getting Started

### 📋 Clone the Repository
1) Open desired directory in command prompt
2) Clone the repository using the command below

    ```sh
    git clone https://github.com/KevinTrinh1227/Hycord-Bot.git
    ```

### 🛠 set-up
1. Create a "`.env`" file with your tokens and API keys

   ```sh
   DISCORD_BOT_TOKEN=<YOUR_DISCORD_BOT_TOKEN>
   HYPIXEL_API_KEY=<YOUR_HYPIXEL_API_KEY>
   ```

2. Configure the config.json file appropriately

   ```sh
   {
      "general": {
         "bot_prefix": "!",
         "embed_color": "#ff0000",
         "discord_server_guild_id": "YOUR_GUILD_ID"
      },
      "features": {
         "filtered_chat": 0,
         "auto_gexp": 0,
         "inactivity_cmd": 1,
         "punishments_cmd": 1
      },
      "category_ids": {
         "tickets_category": "YOUR_TICKETS_CATEGORY_ID"
      },
      "voice_channel_ids": {
         "member_count": "YOUR_MEMBER_COUNT_CHANNEL_ID",
         "members_online": "YOUR_MEMBERS_ONLINE_CHANNEL_ID",
         "guild_member_online": "YOUR_GUILD_MEMBER_ONLINE_CHANNEL_ID"
      },
      "text_channel_ids": {
         "welcome": "YOUR_WELCOME_CHANNEL_ID",
         "rules": "YOUR_RULES_CHANNEL_ID",
         "inactivity_notice": "YOUR_INACTIVITY_NOTICE_CHANNEL_ID",
         "staff_chat": "YOUR_STAFF_CHAT_CHANNEL_ID",
         "tickets_transcripts": "YOUR_TICKETS_TRANSCRIPTS_CHANNEL_ID",
         "leave_messages": "YOUR_LEAVE_MESSAGES_CHANNEL_ID",
         "daily_guild_points": "YOUR_DAILY_GUILD_POINTS_CHANNEL_ID"
      },
      "role_ids": {
         "guild_member": "YOUR_GUILD_MEMBER_ROLE_ID",
         "verified_member": "YOUR_VERIFIED_MEMBER_ROLE_ID",
         "unverified_member": "YOUR_UNVERIFIED_MEMBER_ROLE_ID",
         "staff_member": "YOUR_STAFF_MEMBER_ROLE_ID",
         "bots": "YOUR_BOTS_ROLE_ID"
      },
      "hypixel_ids": {
         "guild_id": "YOUR_HYPIXEL_GUILD_ID"
      }
   }
   ```

3. Install dependencies

   ```sh
   pip install discord.py
   ```
   ```sh
   pip install python-dotenv
   ```
   ```sh
   pip install requests
   ```
   ```sh
   pip install pytz
   ```
   ```sh
   pip chat-exporter
   ```
### 🚀 activate bot in terminal

1. build and run Discord bot

   ```sh
   python main.py
   ```
