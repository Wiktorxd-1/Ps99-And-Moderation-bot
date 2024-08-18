import discord
import requests
from discord.ext import tasks, commands
from discord import app_commands
from datetime import datetime, timezone
import asyncio

TOKEN = 'Your Bot Token ;)' 
OWNER_ID = 697047593334603837 # Change to your user id 
SERVER_ID = 1208706536684130354 # Change to the server your gonna use the bot in (I'ma update the code soon to work better)
ROLE_ID = 1256972069103734865 # Your staff role 

CHANNEL_ID_PET_SIM = 1270334660957700139 # Change to your channel to update the ps99 stats
GAME_UNIVERSE_ID_PET_SIM = 3317771874

API_URL_PET_SIM = f"https://games.roblox.com/v1/games?universeIds={GAME_UNIVERSE_ID_PET_SIM}"
POINTS_API_URL = 'https://biggamesapi.io/api/clans?page=1&pageSize=10&sort=Points&sortOrder=desc'
DIAMONDS_API_URL = 'https://biggamesapi.io/api/clans?page=1&pageSize=10&sort=DepositedDiamonds&sortOrder=desc'

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

async def check_role(interaction: discord.Interaction):
    if interaction.guild and interaction.guild.id == SERVER_ID:
        role = discord.utils.get(interaction.guild.roles, id=ROLE_ID)
        if role not in interaction.user.roles and interaction.user.id != OWNER_ID:
            await interaction.response.send_message(embed=discord.Embed(
                title="Error",
                description="You do not have the required role to use this command in this server.",
                color=discord.Color.red()
            ))
            return False
    return True

@bot.tree.command(name="ban", description="Ban a user.")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not check_permissions(interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        ))
        return
    
    if not await check_role(interaction):
        return

    try:
        await member.ban(reason=reason)
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
    if not check_permissions(interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        ))
        return
    
    if not await check_role(interaction):
        return

    try:
        await member.kick(reason=reason)
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
@commands.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    if interaction.user.id == OWNER_ID:
        has_permission = True
    else:
        role = discord.utils.get(interaction.guild.roles, id=ROLE_ID)
        has_permission = role in interaction.user.roles

    if not has_permission:
        await interaction.response.send_message('You do not have the required role or permission to use this command.\n-# Made By Mee69_2  TYSM!', ephemeral=True)
        return

    if amount < 1:
        await interaction.response.send_message('Please specify a number greater than 0.\n-# Made By Mee69_2  TYSM!', ephemeral=True)
        return

    await interaction.response.send_message('Deleting messages...\n-# Made By Mee69_2  TYSM!', ephemeral=True)

    try:
        deleted = await interaction.channel.purge(limit=amount + 1)
        confirmation_message = await interaction.followup.send(f'Deleted {len(deleted) - 1} messages.\n-# Made By Mee69_2  TYSM!', ephemeral=True)
        await confirmation_message.delete(delay=30)
    except discord.Forbidden:
        error_message = await interaction.followup.send('I do not have permissions to delete messages in this channel.\n-# Made By Mee69_2  TYSM!', ephemeral=True)
        await error_message.delete(delay=30)
    except discord.HTTPException as e:
        error_message = await interaction.followup.send(f'Failed to delete messages: {str(e)}\n-# Made By Mee69_2  TYSM!', ephemeral=True)
        await error_message.delete(delay=30)


@bot.tree.command(name="slowmode", description="Set the slowmode for the current channel.")
async def slowmode(interaction: discord.Interaction, seconds: int):
    if not check_permissions(interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        ))
        return

    if not await check_role(interaction):
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

@bot.tree.command(name="dm", description="DM a user.")
async def dm(interaction: discord.Interaction, user_id: str, *, message: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        ))
        return

    if not user_id.isdigit():
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="Please provide a valid numeric user ID.",
            color=discord.Color.red()
        ))
        return

    user_id = int(user_id)

    try:
        user = await bot.fetch_user(user_id)
        await user.send(message)
        await interaction.response.send_message(embed=discord.Embed(
            title="DM Sent",
            description=f"Message sent to {user}.",
            color=discord.Color.green()
        ))
    except discord.NotFound:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="User not found.",
            color=discord.Color.red()
        ))
    except discord.Forbidden:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description="I do not have permission to send a DM to this user.",
            color=discord.Color.red()
        ))
    except discord.HTTPException as e:
        await interaction.response.send_message(embed=discord.Embed(
            title="Error",
            description=f"An unexpected error occurred: {e}",
            color=discord.Color.red()
        ))

@bot.tree.command(name="best-clans", description="Displays the top clans based on points or diamonds.")
@app_commands.choices(
    sort_by=[
        app_commands.Choice(name="Points", value="points"),
        app_commands.Choice(name="Diamonds", value="diamonds"),
    ]
)
async def best_clans(interaction: discord.Interaction, sort_by: app_commands.Choice[str]):
    api_url = POINTS_API_URL if sort_by.value == "points" else DIAMONDS_API_URL
    await interaction.response.defer()
    clans = await fetch_top_clans(api_url)
    if not clans:
        await interaction.followup.send("Failed to fetch clans. Please try again later.")
        return
    embed = discord.Embed(
        title=f"Top Clans by {'Points' if sort_by.value == 'points' else 'Diamonds'}",
        description=f"Here are the top 10 clans based on {'points' if sort_by.value == 'points' else 'diamonds'}:",
        color=discord.Color.gold()
    )
    for index, clan in enumerate(clans, start=1):
        points = clan.get('Points', 0)
        deposited_diamonds = clan.get('DepositedDiamonds', 0)
        country_code = clan.get('CountryCode', 'Unknown')
        country_name, country_emoji = get_country_info(country_code)
        points_formatted = f"{points:,}"
        diamonds_formatted = f"{deposited_diamonds:,}"

        description = (
            f"⭐ Points: {points_formatted}\n"
            f"💎 Diamonds: {diamonds_formatted}\n"
            f"👥 Members: {clan.get('Members', 'Unknown')}\n"
            f"🌍 Country: {country_name} {country_emoji}\n"
        )
        embed.add_field(name=f"Place: #{index}", value=description, inline=False)

    await interaction.followup.send(embed=embed)

async def fetch_top_clans(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.RequestException as e:
        print(f"Error fetching clans: {e}")
        return []

def get_country_info(country_code):
    return COUNTRY_DATA.get(country_code.upper(), ("Unknown", "🏳"))

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
        
        if game_name == "Pet Simulator":
            stats_message_content = f"# Pet Simulator Stats\n🎮 **Players**: {og_player_count:,}\n⭐ **Favorites**: {last_favorite_count:,}\n➡️ **Visits**: {last_visit_count:,}"
            update_message_content = f"🆕  **Pet Simulator Update Info**\n⌛ **Last update**: {relative_time}\n📅 **Date**: {formatted_time}"
            global stats_message_id_ps99, update_message_id_ps99
        
        stats_message = await channel.send(stats_message_content)
        if game_name == "Pet Simulator":
            stats_message_id_ps99 = stats_message.id
            
        await asyncio.sleep(1)
        update_message = await channel.send(update_message_content)
        if game_name == "Pet Simulator":
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

bot.run(TOKEN)
