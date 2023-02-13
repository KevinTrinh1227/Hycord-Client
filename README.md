<p align="center">
  <img src="https://user-images.githubusercontent.com/48145892/218457340-39c08f69-e027-4529-b907-b2414435af77.png"><br>
  Visit the <a href="https://www.hycord.netlify.app" target="_blank">Hycord Project Page</a> for more information.<hr>
</p>

<p>
  Hycord is essentially a <strong>Discord python</strong> program that is targeted toward Java Minecraft players who play on Hypixel. This bot is an all-in-one easy-to-use/setup bot that allows anyone to have their own fully customizable bot. This bot uses numerous APIs such as <strong><a href="https://api.hypixel.net/" target="_blank">Hypixel</a></strong> and <strong><a href="https://playerdb.co/" target="_blank">PlayerDB</a></strong> not only to retrieve player data but to also validate and allow users to verify/sync their accounts together. This is currently an active project that will continuously receive updates, changes, and bug fixes. So be on the lookup for <strong><a href="https://github.com/KevinTrinh1227/Hycord-Bot/commits/main" target="_blank">new updates</a></strong>.
</p>

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
    "bot_prefix": "<DESIRED_PREEFIX>",
    "embed_color": "<HEX_COLOR_CODE>",
    }
   ```

3. Install the modules

   ```sh
   pip install discord.py
   ```
   ```sh
   pip install python-dotenv
   ```
   ```sh
   pip install requests
   ```

### 🚀 activate bot in terminal

1. build and run Discord bot

   ```sh
   python main.py
   ```
