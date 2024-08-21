## Read Me

## Needed

- Python 3.8 or higher
- `discord.py` library
- `requests` libary
- `aiohttp` libary
- Discord bot token

## Installation

1. Install Python and Pip if you haven't already.
2. Download discord.py and requests
 ```bash
   pip install discord.py requests aiohttp
   ```
3. Copy the main.py and paste into your editor.


## Configuration

Open the script and update the following variables:

   ```python
TOKEN = 'Your token'
OWNER_ID = 697047593334603837 # Change to your id,! i need to fix where the owner can use all commands add your id also to ALLOWED_ADMIN_USER_IDS!
SERVER_ID = 1208706536684130354 # Change to server id the bot is gonna mainly be gonna used in
ROLE_ID = 1256972069103734865 # Staff role of your server where you gonna use it in (set to None if you dont want it)
CHANNEL_ID_PET_SIM = 1270334660957700139 # Channel to send the ps99 stats to
ALLOWED_ADMIN_USER_IDS = [None]  # Use , and a space to spearate (set to None if you dont want it)
   ```

## Bot Commands

### Admin Commands
- `/ban <user> [reason]`: Ban a user from the server.
- `/kick <user> [reason]`: Kick a user from the server.
- `/dm <user_id> <message>`: Send a direct message to a user using their ID.
- `/clear <amount>`: Clear a specified number of messages in the channel.
- `/slowmode <seconds>`: Set slow mode for the current channel.

### General Commands
- `/ping`: Check the bot's latency.
- `/avatar [user]`: Get the avatar of a specified user or yourself.
- `/best-clans <points|diamonds>`: Display the top clans based on points or diamonds.
- `/clan-info [clan name]`: Get Clan Information.
- `/admin-perm-check`: Check if you can use admin commands.

## Contribution

Feel free to contribute to this project by reporting issues or submitting pull requests.


---

For any issues or questions, please dm me on discord username: Wiktorxd_1
