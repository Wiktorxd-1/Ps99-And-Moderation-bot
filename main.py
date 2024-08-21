import discord
import requests
import asyncio
import aiohttp
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timezone

TOKEN = 'Your token'
OWNER_ID = 697047593334603837 # Change to your id,! i need to fix where the owner can use all commands add your id also to ALLOWED_ADMIN_USER_IDS!
SERVER_ID = 1208706536684130354 # Change to server id the bot is gonna mainly be gonna used in
ROLE_ID = 1256972069103734865 # Staff role of your server where you gonna use it in (set to None if you dont want it)
CHANNEL_ID_PET_SIM = 1270334660957700139 # Channel to send the ps99 stats to


POINTS_API_URL = 'https://biggamesapi.io/api/clans?page={page}&pageSize=10&sort=Points&sortOrder=desc'
DIAMONDS_API_URL = 'https://biggamesapi.io/api/clans?page={page}&pageSize=10&sort=DepositedDiamonds&sortOrder=desc'
API_URL_PET_SIM = f"https://games.roblox.com/v1/games?universeIds=3317771874"

ALLOWED_ADMIN_USER_IDS = [None]  # Use , and a space to spearate (set to None if you dont want it)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=':', intents=intents)

start_time = datetime.now(timezone.utc)
update_message_id_ps99 = None
stats_message_id_ps99 = None

COUNTRY_DATA = {
    "AF": ("Afghanistan", "🇦🇫"),
    "AL": ("Albania", "🇦🇱"),
    "DZ": ("Algeria", "🇩🇿"),
    "AS": ("American Samoa", "🇦🇸"),
    "AD": ("Andorra", "🇦🇩"),
    "AO": ("Angola", "🇦🇴"),
    "AI": ("Anguilla", "🇦🇮"),
    "AQ": ("Antarctica", "🇦🇶"),
    "AG": ("Antigua and Barbuda", "🇦🇬"),
    "AR": ("Argentina", "🇦🇷"),
    "AM": ("Armenia", "🇦🇲"),
    "AW": ("Aruba", "🇦🇼"),
    "AU": ("Australia", "🇦🇺"),
    "AT": ("Austria", "🇦🇹"),
    "AZ": ("Azerbaijan", "🇦🇿"),
    "BS": ("Bahamas", "🇧🇸"),
    "BH": ("Bahrain", "🇧🇭"),
    "BD": ("Bangladesh", "🇧🇩"),
    "BB": ("Barbados", "🇧🇧"),
    "BY": ("Belarus", "🇧🇾"),
    "BE": ("Belgium", "🇧🇪"),
    "BZ": ("Belize", "🇧🇿"),
    "BJ": ("Benin", "🇧🇯"),
    "BM": ("Bermuda", "🇦🇲"),
    "BT": ("Bhutan", "🇧🇹"),
    "BO": ("Bolivia", "🇧🇴"),
    "BQ": ("Bonaire, Sint Eustatius and Saba", "🇧🇶"),
    "BA": ("Bosnia and Herzegovina", "🇧🇦"),
    "BW": ("Botswana", "🇧🇼"),
    "BV": ("Bouvet Island", "🇧🇻"),
    "BR": ("Brazil", "🇧🇷"),
    "IO": ("British Indian Ocean Territory", "🇮🇴"),
    "BN": ("Brunei Darussalam", "🇧🇳"),
    "BG": ("Bulgaria", "🇧🇬"),
    "BF": ("Burkina Faso", "🇧🇫"),
    "BI": ("Burundi", "🇧🇮"),
    "CV": ("Cabo Verde", "🇨🇻"),
    "KH": ("Cambodia", "🇰🇭"),
    "CM": ("Cameroon", "🇨🇲"),
    "CA": ("Canada", "🇨🇦"),
    "IC": ("Canary Islands", "🇮🇨"),
    "KY": ("Cayman Islands", "🇰🇾"),
    "CF": ("Central African Republic", "🇨🇫"),
    "TD": ("Chad", "🇹🇩"),
    "CL": ("Chile", "🇨🇱"),
    "CN": ("China", "🇨🇳"),
    "CX": ("Christmas Island", "🇨🇽"),
    "CC": ("Cocos (Keeling) Islands", "🇨🇨"),
    "CO": ("Colombia", "🇨🇴"),
    "KM": ("Comoros", "🇰🇲"),
    "CD": ("Congo, Democratic Republic of the", "🇨🇩"),
    "CG": ("Congo, Republic of the", "🇨🇬"),
    "CK": ("Cook Islands", "🇰🇰"),
    "CR": ("Costa Rica", "🇨🇷"),
    "HR": ("Croatia", "🇭🇷"),
    "CU": ("Cuba", "🇨🇺"),
    "CW": ("Curaçao", "🇨🇼"),
    "CY": ("Cyprus", "🇨🇾"),
    "CZ": ("Czech Republic", "🇨🇿"),
    "DK": ("Denmark", "🇩🇰"),
    "DJ": ("Djibouti", "🇩🇯"),
    "DM": ("Dominica", "🇩🇲"),
    "DO": ("Dominican Republic", "🇩🇴"),
    "EC": ("Ecuador", "🇪🇨"),
    "EG": ("Egypt", "🇪🇬"),
    "SV": ("El Salvador", "🇸🇻"),
    "GQ": ("Equatorial Guinea", "🇬🇶"),
    "ER": ("Eritrea", "🇪🇷"),
    "EE": ("Estonia", "🇪🇪"),
    "SZ": ("Eswatini", "🇸🇿"),
    "ET": ("Ethiopia", "🇪🇹"),
    "FK": ("Falkland Islands", "🇫🇰"),
    "FO": ("Faroe Islands", "🇫🇴"),
    "FJ": ("Fiji", "🇫🇯"),
    "FI": ("Finland", "🇫🇮"),
    "FR": ("France", "🇫🇷"),
    "GF": ("French Guiana", "🇬🇫"),
    "PF": ("French Polynesia", "🇵🇫"),
    "TF": ("French Southern Territories", "🇹🇫"),
    "GA": ("Gabon", "🇬🇦"),
    "GM": ("Gambia", "🇬🇲"),
    "GE": ("Georgia", "🇬🇪"),
    "DE": ("Germany", "🇩🇪"),
    "GH": ("Ghana", "🇬🇭"),
    "GI": ("Gibraltar", "🇬🇮"),
    "GR": ("Greece", "🇬🇷"),
    "GL": ("Greenland", "🇬🇱"),
    "GD": ("Grenada", "🇬🇩"),
    "GP": ("Guadeloupe", "🇬🇵"),
    "GU": ("Guam", "🇬🇺"),
    "GT": ("Guatemala", "🇬🇹"),
    "GG": ("Guernsey", "🇬🇬"),
    "GN": ("Guinea", "🇬🇳"),
    "GW": ("Guinea-Bissau", "🇬🇼"),
    "GY": ("Guyana", "🇬🇾"),
    "HT": ("Haiti", "🇭🇹"),
    "HM": ("Heard Island and McDonald Islands", "🇭🇲"),
    "VA": ("Holy See", "🇻🇦"),
    "HN": ("Honduras", "🇭🇳"),
    "HK": ("Hong Kong", "🇭🇰"),
    "HU": ("Hungary", "🇭🇺"),
    "IS": ("Iceland", "🇮🇸"),
    "IN": ("India", "🇮🇳"),
    "ID": ("Indonesia", "🇮🇩"),
    "IR": ("Iran", "🇮🇷"),
    "IQ": ("Iraq", "🇮🇶"),
    "IE": ("Ireland", "🇮🇪"),
    "IM": ("Isle of Man", "🇮🇲"),
    "IL": ("Israel", "🇮🇱"),
    "IT": ("Italy", "🇮🇹"),
    "JM": ("Jamaica", "🇯🇲"),
    "JP": ("Japan", "🇯🇵"),
    "JE": ("Jersey", "🇯🇪"),
    "JO": ("Jordan", "🇯🇴"),
    "KZ": ("Kazakhstan", "🇰🇿"),
    "KE": ("Kenya", "🇰🇪"),
    "KI": ("Kiribati", "🇰🇮"),
    "KP": ("Korea, Democratic People's Republic of", "🇰🇵"),
    "KR": ("Korea, Republic of", "🇰🇷"),
    "KW": ("Kuwait", "🇰🇼"),
    "KG": ("Kyrgyzstan", "🇰🇬"),
    "LA": ("Lao People's Democratic Republic", "🇱🇦"),
    "LV": ("Latvia", "🇱🇻"),
    "LB": ("Lebanon", "🇱🇧"),
    "LS": ("Lesotho", "🇱🇸"),
    "LR": ("Liberia", "🇱🇷"),
    "LY": ("Libya", "🇱🇾"),
    "LI": ("Liechtenstein", "🇱🇮"),
    "LT": ("Lithuania", "🇱🇹"),
    "LU": ("Luxembourg", "🇱🇺"),
    "MO": ("Macao", "🇲🇴"),
    "MG": ("Madagascar", "🇲🇬"),
    "MW": ("Malawi", "🇲🇼"),
    "MY": ("Malaysia", "🇲🇾"),
    "MV": ("Maldives", "🇲🇻"),
    "ML": ("Mali", "🇲🇱"),
    "MT": ("Malta", "🇲🇹"),
    "MH": ("Marshall Islands", "🇲🇭"),
    "MQ": ("Martinique", "🇲🇶"),
    "MR": ("Mauritania", "🇲🇷"),
    "MU": ("Mauritius", "🇲🇺"),
    "YT": ("Mayotte", "🇾🇹"),
    "MX": ("Mexico", "🇲🇽"),
    "FM": ("Micronesia", "🇫🇲"),
    "MD": ("Moldova", "🇲🇩"),
    "MC": ("Monaco", "🇲🇨"),
    "MN": ("Mongolia", "🇲🇳"),
    "ME": ("Montenegro", "🇲🇪"),
    "MS": ("Montserrat", "🇲🇸"),
    "MA": ("Morocco", "🇲🇦"),
    "MZ": ("Mozambique", "🇿🇦"),
    "MM": ("Myanmar", "🇲🇲"),
    "NA": ("Namibia", "🇳🇦"),
    "NR": ("Nauru", "🇦🇷"),
    "NP": ("Nepal", "🇳🇵"),
    "NL": ("Netherlands", "🇳🇱"),
    "NC": ("New Caledonia", "🇳🇨"),
    "NZ": ("New Zealand", "🇳🇿"),
    "NI": ("Nicaragua", "🇳🇮"),
    "NE": ("Niger", "🇳🇪"),
    "NG": ("Nigeria", "🇳🇬"),
    "NU": ("Niue", "🇳🇺"),
    "NF": ("Norfolk Island", "🇳🇫"),
    "MP": ("Northern Mariana Islands", "🇲🇵"),
    "NO": ("Norway", "🇳🇴"),
    "OM": ("Oman", "🇴🇲"),
    "PK": ("Pakistan", "🇵🇰"),
    "PW": ("Palau", "🇵🇼"),
    "PS": ("Palestine", "🇵🇸"),
    "PA": ("Panama", "🇵🇦"),
    "PG": ("Papua New Guinea", "🇵🇬"),
    "PY": ("Paraguay", "🇵🇾"),
    "PE": ("Peru", "🇵🇪"),
    "PH": ("Philippines", "🇵🇭"),
    "PN": ("Pitcairn", "🇵🇳"),
    "PL": ("Poland", "🇵🇱"),
    "PT": ("Portugal", "🇵🇹"),
    "PR": ("Puerto Rico", "🇵🇷"),
    "QA": ("Qatar", "🇶🇦"),
    "RE": ("Réunion", "🇷🇪"),
    "RO": ("Romania", "🇷🇴"),
    "RU": ("Russia", "🇷🇺"),
    "RW": ("Rwanda", "🇷🇼"),
    "BL": ("Saint Barthélemy", "🇧🇱"),
    "SH": ("Saint Helena", "🇸🇭"),
    "KN": ("Saint Kitts and Nevis", "🇰🇳"),
    "LC": ("Saint Lucia", "🇱🇨"),
    "MF": ("Saint Martin", "🇲🇫"),
    "SX": ("Sint Maarten", "🇸🇽"),
    "SV": ("Saint Vincent and the Grenadines", "🇻🇨"),
    "WS": ("Samoa", "🇼🇸"),
    "SM": ("San Marino", "🇸🇲"),
    "ST": ("Sao Tome and Principe", "🇸🇹"),
    "SA": ("Saudi Arabia", "🇸🇦"),
    "SN": ("Senegal", "🇸🇳"),
    "RS": ("Serbia", "🇷🇸"),
    "SC": ("Seychelles", "🇸🇨"),
    "SL": ("Sierra Leone", "🇸🇱"),
    "SG": ("Singapore", "🇸🇬"),
    "SK": ("Slovakia", "🇸🇰"),
    "SI": ("Slovenia", "🇸🇮"),
    "SB": ("Solomon Islands", "🇸🇧"),
    "SO": ("Somalia", "🇸🇴"),
    "ZA": ("South Africa", "🇿🇦"),
    "GS": ("South Georgia and the South Sandwich Islands", "🇬🇸"),
    "SS": ("South Sudan", "🇸🇸"),
    "ES": ("Spain", "🇪🇸"),
    "LK": ("Sri Lanka", "🇱🇰"),
    "SD": ("Sudan", "🇸🇩"),
    "SR": ("Suriname", "🇸🇷"),
    "SJ": ("Svalbard and Jan Mayen", "🇸🇯"),
    "SZ": ("Eswatini", "🇸🇿"),
    "SE": ("Sweden", "🇸🇪"),
    "CH": ("Switzerland", "🇨🇭"),
    "SY": ("Syrian Arab Republic", "🇸🇾"),
    "TW": ("Taiwan", "🇹🇼"),
    "TJ": ("Tajikistan", "🇹🇯"),
    "TZ": ("Tanzania, United Republic of", "🇹🇿"),
    "TH": ("Thailand", "🇹🇭"),
    "TL": ("Timor-Leste", "🇹🇱"),
    "TG": ("Togo", "🇹🇬"),
    "TK": ("Tokelau", "🇹🇰"),
    "TO": ("Tonga", "🇹🇴"),
    "TT": ("Trinidad and Tobago", "🇹🇹"),
    "TN": ("Tunisia", "🇹🇳"),
    "TR": ("Turkey", "🇹🇷"),
    "TM": ("Turkmenistan", "🇹🇲"),
    "TC": ("Turks and Caicos Islands", "🇹🇨"),
    "TV": ("Tuvalu", "🇹🇻"),
    "UG": ("Uganda", "🇺🇬"),
    "UA": ("Ukraine", "🇺🇦"),
    "AE": ("United Arab Emirates", "🇦🇪"),
    "GB": ("United Kingdom", "🇬🇧"),
    "US": ("United States", "🇺🇸"),
    "UY": ("Uruguay", "🇺🇾"),
    "UZ": ("Uzbekistan", "🇺🇿"),
    "VU": ("Vanuatu", "🇻🇺"),
    "VE": ("Venezuela", "🇻🇪"),
    "VN": ("Vietnam", "🇻🇳"),
    "WF": ("Wallis and Futuna", "🇼🇫"),
    "EH": ("Western Sahara", "🇪🇭"),
    "YE": ("Yemen", "🇾🇪"),
    "ZM": ("Zambia", "🇿🇲"),
    "ZW": ("Zimbabwe", "🇿🇼"),
}


def fetch_game_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            return data['data'][0]
    return None

async def fetch_top_clans(api_url):
    try:
        response = requests.get(api_url)
        return response.json().get('data', [])
    except requests.RequestException as e:
        print(f"Error fetching clans: {e}")
        return []

def get_country_info(country_code):
    return COUNTRY_DATA.get(country_code.upper(), ("Unknown", "🏳"))

def is_valid_clan_name(clan_name: str) -> bool:
    return len(clan_name) <= 4

async def fetch_clan_info(clan_name):
    url = f"https://biggamesapi.io/api/clan/{clan_name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None
        
async def fetch_username(userid):
    url = f"https://users.roblox.com/v1/users/{userid}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                user_data = await response.json()
                return user_data.get("name"), user_data.get("id")
            return None, None
                
async def fetch_clan_names():
    url = "https://biggamesapi.io/api/clansList"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    global valid_clan_names
                    valid_clan_names = data.get('data', [])
                else:
                    print("Failed to fetch clan names.")
    except Exception as e:
        print(f"Error fetching clan names: {e}")                

class ClanPagination(discord.ui.View):
    def __init__(self, api_url, message):
        super().__init__(timeout=600)
        self.api_url = api_url
        self.page = 1
        self.message = message

    @staticmethod
    def format_number(n):
        if n >= 1_000_000_000:
            return f"{n / 1_000_000_000:.1f}B"
        elif n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M"
        elif n >= 1_000:
            return f"{n / 1_000:.1f}K"
        else:
            return str(n)

    async def show_clans(self):
        clans = await fetch_top_clans(self.api_url.format(page=self.page))
        if not clans:
            await self.message.edit(content="No clans found!", embed=None, view=None)
            return
        
        embed = discord.Embed(
            title="Top Clans",
            description=f"Here are the clans from page {self.page}:",
            color=discord.Color.gold()
        )

        for index, clan in enumerate(clans, start=1):
            clan_name = clan.get('Name', 'Unknown Clan')
            points = clan.get('Points', 0)
            deposited_diamonds = clan.get('DepositedDiamonds', 0)
            country_code = clan.get('CountryCode', 'Unknown')
            country_name, country_emoji = get_country_info(country_code)

            points_formatted = self.format_number(points)
            diamonds_formatted = self.format_number(deposited_diamonds)

            description = (
                f"⭐ Points: {points_formatted}\n"
                f"💎 Diamonds: {diamonds_formatted}\n"
                f"👥 Members: {clan.get('Members', 'Unknown')}\n"
                f"🌍 Country: {country_name} {country_emoji}\n"
            )
            embed.add_field(name=f"{clan_name} (Place: #{(self.page - 1) * 10 + index})", value=description, inline=False)

        await self.message.edit(content="", embed=embed, view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            if self.page > 1:
                self.page -= 1
                await self.show_clans()
                await interaction.response.defer()
            else:
                await interaction.response.send_message("You are already on the first page.", ephemeral=True)
        except Exception:
            pass

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            next_page_clans = await fetch_top_clans(self.api_url.format(page=self.page + 1))
            if not next_page_clans:
                await interaction.response.send_message("There are no more clans to show.", ephemeral=True)
            else:
                self.page += 1
                await self.show_clans()
                await interaction.response.defer() 
        except Exception:
            pass

@bot.tree.command(name="best-clans", description="Displays the top clans based on points or diamonds.")
@app_commands.choices(sort_by=[
    app_commands.Choice(name="Points", value="points"),
    app_commands.Choice(name="Diamonds", value="diamonds"),
])
async def best_clans(interaction: discord.Interaction, sort_by: app_commands.Choice[str]):
    api_url = POINTS_API_URL if sort_by.value == "points" else DIAMONDS_API_URL
    await interaction.response.send_message(content="Loading clans...", ephemeral=False)
    loading_message = await interaction.original_response()
    view = ClanPagination(api_url, loading_message)
    await view.show_clans()

async def initial_check(channel, api_url, game_name):
    await clear_channel(channel)
    game_data = fetch_game_data(api_url)
    
    if game_data:
        updated_time_str = game_data['updated']
        last_update_time = datetime.fromisoformat(updated_time_str.replace("Z", "+00:00"))
        og_player_count = game_data['playing']
        last_favorite_count = game_data['favoritedCount']
        last_visit_count = game_data['visits']
        relative_time, formatted_time = format_discord_timestamp(last_update_time)       
        stats_message_content = f"# {game_name} Stats\n🎮 **Players**: {og_player_count:,}\n⭐ **Favorites**: {last_favorite_count:,}\n➡️ **Visits**: {last_visit_count:,}"
        update_message_content = f"🆕  **{game_name} Update Info**\n⌛ **Last update**: {relative_time}\n📅 **Date**: {formatted_time}"

        stats_message = await channel.send(stats_message_content)
        global stats_message_id_ps99
        stats_message_id_ps99 = stats_message.id

        await asyncio.sleep(1)
        update_message = await channel.send(update_message_content)
        global update_message_id_ps99
        update_message_id_ps99 = update_message.id

@tasks.loop(seconds=13)
async def check_for_updates():
    global update_message_id_ps99, stats_message_id_ps99
    channel_ps99 = bot.get_channel(CHANNEL_ID_PET_SIM)
    game_data_ps99 = fetch_game_data(API_URL_PET_SIM)
    
    if game_data_ps99:
        updated_time_str = game_data_ps99['updated']
        new_update_time = datetime.fromisoformat(updated_time_str.replace("Z", "+00:00"))
        og_player_count = game_data_ps99['playing']
        new_favorite_count = game_data_ps99['favoritedCount']
        new_visit_count = game_data_ps99['visits']

        if update_message_id_ps99:
            relative_time, formatted_time = format_discord_timestamp(new_update_time)
            update_message_content = f"🆕  **Pet Simulator Update Info**\n⌛ **Last update**: {relative_time}\n📅 **Date**: {formatted_time}"
            try:
                message = await channel_ps99.fetch_message(update_message_id_ps99)
                await message.edit(content=update_message_content)
            except discord.NotFound:
                new_message = await channel_ps99.send(update_message_content)
                update_message_id_ps99 = new_message.id

        stats_message_content = f"# Pet Simulator Stats\n🎮 **Players**: {og_player_count:,}\n⭐ **Favorites**: {new_favorite_count:,}\n➡️ **Visits**: {new_visit_count:,}"
        if stats_message_id_ps99:
            try:
                message = await channel_ps99.fetch_message(stats_message_id_ps99)
                await message.edit(content=stats_message_content)
            except discord.NotFound:
                new_message = await channel_ps99.send(stats_message_content)
                stats_message_id_ps99 = new_message.id

@tasks.loop(seconds=1)
async def update_uptime():
    now = datetime.now(timezone.utc)
    uptime = now - start_time
    uptime_str = f'Uptime: {format_uptime(uptime)}'
    try:
        await bot.change_presence(activity=discord.Game(name=uptime_str))
    except Exception as e:
        print(f'Error updating presence: {e}')

@tasks.loop(seconds=360)
async def sync_commands():
    await bot.tree.sync()
    print("Commands synced with Discord.")

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    update_uptime.start()
    sync_commands.start()
    channel_ps99 = bot.get_channel(CHANNEL_ID_PET_SIM)
    await initial_check(channel_ps99, API_URL_PET_SIM, "Pet Simulator")
    check_for_updates.start()
    await fetch_clan_names()

async def clear_channel(channel):
    try:
        await channel.purge(limit=100)
    except discord.Forbidden:
        print("I do not have permission to clear messages in this channel.")
    except discord.HTTPException as e:
        print(f"Failed to clear channel messages: {e}")

def format_discord_timestamp(dt):
    timestamp = int(dt.timestamp())
    return f"<t:{timestamp}:R>", f"<t:{timestamp}:f>"

def format_uptime(uptime):
    seconds = int(uptime.total_seconds())
    periods = [
        ('month', 60 * 60 * 24 * 30),
        ('day', 60 * 60 * 24),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1)
    ]
    strings = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value > 0:
                strings.append(f"{period_value} {period_name}{'s' if period_value > 1 else ''}")
    return ", ".join(strings)

def check_permissions(interaction: discord.Interaction):
    return interaction.user.id == OWNER_ID

async def is_admin(interaction: discord.Interaction):
    if interaction.guild is None:
        return False

    role = discord.utils.get(interaction.guild.roles, id=ROLE_ID)
    if role in interaction.user.roles or interaction.user.id in ALLOWED_ADMIN_USER_IDS:
        return True

    return False

@bot.tree.command(name="admin-perm-check", description="Check if you can use admin commands.")
async def admin_info(interaction: discord.Interaction):
    if await is_admin(interaction):
        await interaction.response.send_message("You are allowed to use admin commands!", ephemeral=True)
    else:
        await interaction.response.send_message("You are not allowed to use admin commands.", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a user.")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if interaction.guild is None:
        await interaction.response.send_message("You can't use this command in DMs.", ephemeral=True)
        return

    if not await is_admin(interaction):
        await interaction.response.send_message("You aren't allowed to use admin commands.", ephemeral=True)
        return

    if reason is None:
        reason = "No reason provided"
    
    formatted_reason = f"{reason} | Banned By {interaction.user.name}"
    try:
        await member.ban(reason=formatted_reason)
        await interaction.response.send_message(embed=discord.Embed(
            title="Banned",
            description=f"User {member} has been banned.",
            color=discord.Color.green()
        ))
    except discord.Forbidden:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="I do not have permission to ban this user.",
            color=discord.Color.red()
        ))
    except discord.HTTPException as e:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description=f"An unexpected error occurred: {e}",
            color=discord.Color.red()
        ))

@bot.tree.command(name="kick", description="Kick a user.")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if interaction.guild is None:
        await interaction.response.send_message("You can't use this command in DMs.", ephemeral=True)
        return

    if not await is_admin(interaction):
        await interaction.response.send_message("You aren't allowed to use admin commands.", ephemeral=True)
        return

    if reason is None:
        reason = "No reason provided"
    
    formatted_reason = f"{reason} | Kicked By {interaction.user.name}"
    try:
        await member.kick(reason=formatted_reason)
        await interaction.response.send_message(embed=discord.Embed(
            title="Kicked",
            description=f"User {member} has been kicked.",
            color=discord.Color.green()
        ))
    except discord.Forbidden:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="I do not have permission to kick this user.",
            color=discord.Color.red()
        ))
    except discord.HTTPException as e:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description=f"An unexpected error occurred: {e}",
            color=discord.Color.red()
        ))

@bot.tree.command(name="ping", description="Get the bot's latency.")
async def ping(interaction: discord.Interaction):
    bot_ping = round(bot.latency * 1000)
    await interaction.response.send_message(embed=discord.Embed(
        title="🏓 Pong!",
        description=f"**Bot Latency:** {bot_ping}ms",
        color=discord.Color.blue()
    ))

@bot.tree.command(name="avatar", description="Get a user's avatar.")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    avatar_url = member.avatar.url
    await interaction.response.send_message(embed=discord.Embed(
        title=f"{member}'s Avatar",
        description=f"[Click here]({avatar_url}) to view the full-size image.",
        color=discord.Color.blurple()
    ).set_image(url=avatar_url))

@bot.tree.command(name="clear", description="Clear a specific amount of messages in a channel.")
async def clear(interaction: discord.Interaction, amount: int):
    if interaction.guild is None:
        await interaction.response.send_message("You can't use this command in DMs.", ephemeral=True)
        return

    if not await is_admin(interaction):
        await interaction.response.send_message("You aren't allowed to use admin commands.", ephemeral=True)
        return

    if amount < 1:
        await interaction.response.send_message('Please specify a number greater than 0.', ephemeral=True)
        return

    await interaction.response.send_message('Deleting messages...', ephemeral=True)

    try:
        deleted = await interaction.channel.purge(limit=amount + 1)
        confirmation_message = await interaction.followup.send(f'Deleted {len(deleted) - 1} messages.', ephemeral=True)
        await confirmation_message.delete(delay=30)
    except discord.Forbidden:
        error_message = await interaction.followup.send('I do not have permissions to delete messages in this channel.', ephemeral=True)
        await error_message.delete(delay=30)
    except discord.HTTPException as e:
        error_message = await interaction.followup.send(f'Failed to delete messages: {str(e)}.', ephemeral=True)
        await error_message.delete(delay=30)

@bot.tree.command(name="slowmode", description="Set the slowmode for the current channel.")
async def slowmode(interaction: discord.Interaction, seconds: int):
    if interaction.guild is None:
        await interaction.response.send_message("You can't use this command in DMs.", ephemeral=True)
        return

    if not await is_admin(interaction):
        await interaction.response.send_message("You aren't allowed to use admin commands.", ephemeral=True)
        return

    if seconds < 0 or seconds > 21600:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="The slowmode duration must be between 0 and 21600 seconds (6 hours).",
            color=discord.Color.red()
        ))
        return

    try:
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(embed=discord.Embed(
            title="Slowmode Updated",
            description=f"Slowmode has been set to {seconds} seconds.",
            color=discord.Color.green()
        ))
    except discord.Forbidden:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="I do not have permission to change slowmode settings in this channel.",
            color=discord.Color.red()
        ))
    except discord.HTTPException as e:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description=f"An unexpected error occurred: {e}",
            color=discord.Color.red()
        ))

@bot.tree.command(name="bot-info", description="Get information about the bot.")
async def bot_info(interaction: discord.Interaction):
    uptime = format_uptime(datetime.now(timezone.utc) - start_time)
    commands_list = (
        "`best-clans`: Displays the top clans based on points or diamonds.\n"
        "`ban <user> [reason]`: Ban a user.\n"
        "`kick <user> [reason]`: Kick a user.\n"
        "`clear <amount>`: Clear a specific amount of messages in the channel.\n"
        "`slowmode <seconds>`: Set the slowmode for the current channel.\n"
        "`ping`: Check the bot's latency.\n"
        "`avatar [user]`: Get a user's avatar.\n"
        "`bot-info`: Get information about the bot.\n"
        "`admin-perm-check`: Check if you can use admin commands.\n"
    )

    embed = discord.Embed(title="Bot Info", color=discord.Color.blue())
    embed.add_field(name="Owner", value=f"<@{OWNER_ID}>")
    embed.add_field(name="Uptime", value=uptime)
    embed.add_field(name="Bot Commands", value=commands_list)
    embed.set_image(url=bot.user.avatar.url)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clan-info", description="Get clan information.")
async def clan_info(interaction: discord.Interaction, clan_name: str):
    if not is_valid_clan_name(clan_name):
        await interaction.response.send_message("Clan name must be 4 characters or fewer.", ephemeral=True)
        return

    data = await fetch_clan_info(clan_name)
    if data is None or data.get('status') != 'ok':
        await interaction.response.send_message("Clan not found or an error occurred.", ephemeral=True)
        return

    clan_data = data['data']
    country_code = clan_data['CountryCode']
    owner_id = clan_data['Owner']
    
    country_info = COUNTRY_DATA.get(country_code)
    country_name = country_info[0] if country_info else "Unknown Country"
    country_flag = country_info[1] if country_info else "🏳️"
    
    formated_clan_diamonds = ClanPagination.format_number(int(clan_data['DepositedDiamonds']))

    owner_username, owner_userid = await fetch_username(owner_id)
    if owner_username is None:
        owner_info = "Unknown Owner"
    else:
        owner_info = f"[{owner_username}](https://www.roblox.com/users/{owner_userid}/profile)"

    embed = discord.Embed(
        title=f"Clan Info: {clan_data['Name']}",
        description=clan_data['Desc'],
        color=discord.Color.blue()
    )
    
    current_members = len(clan_data['Members'])
    member_capacity = clan_data['MemberCapacity']
    embed.add_field(name="👑 Owner", value=owner_info, inline=True)
    embed.add_field(name="👤 Members", value=f"{current_members}/{member_capacity}", inline=True)
    embed.add_field(name="⭐ Clan Level", value=str(clan_data['GuildLevel']), inline=True)
    embed.add_field(name="💎 Deposited Diamonds", value=formated_clan_diamonds, inline=True)
    embed.add_field(name="🌐  Country", value=f"{country_name} {country_flag}", inline=True)

    icon_url = f"https://biggamesapi.io/image/{clan_data['Icon'].split('//')[-1]}"
    embed.set_thumbnail(url=icon_url)
    
    await interaction.response.send_message(embed=embed)


bot.run(TOKEN)
