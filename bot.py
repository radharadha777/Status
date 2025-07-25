import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import os

# === Settings ===
TOKEN = "MTM4MTMyODM2MzA1MzkxMjA3NA.Gbb0Kp.y96-QuBnYqIdMvWBz7_0VSAIGFcykYdS7_PFPs"
TICKET_CATEGORY_ID = 1393886882668220486  # Replace with your actual Ticket Category ID
GUILD_ID = 1380792281048678441  # Only this server's messages are counted

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === Load message counts ===
message_count = 0
guild_message_count = 0

if os.path.exists("message_count.txt"):
    with open("message_count.txt", "r") as f:
        message_count = int(f.read())

if os.path.exists("guild_message_count.txt"):
    with open("guild_message_count.txt", "r") as f:
        guild_message_count = int(f.read())

status_index = 0

# === Events ===
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    update_status.start()

@bot.event
async def on_message(message):
    global message_count, guild_message_count
    if not message.author.bot:
        message_count += 1

        # Save total message count
        with open("message_count.txt", "w") as f:
            f.write(str(message_count))

        # Count only messages from one specific server
        if message.guild and message.guild.id == GUILD_ID:
            guild_message_count += 1
            with open("guild_message_count.txt", "w") as f:
                f.write(str(guild_message_count))

    await bot.process_commands(message)

# === Bot Status Update ===
@tasks.loop(seconds=20)  # Change status every 20 seconds
async def update_status():
    global status_index

    total_members = sum(g.member_count for g in bot.guilds)
    total_tickets = 0

    for guild in bot.guilds:
        category = discord.utils.get(guild.categories, id=TICKET_CATEGORY_ID)
        if category:
            total_tickets += len([c for c in category.channels if isinstance(c, discord.TextChannel)])

    statuses = [
        f"Tickets: {total_tickets}",
        f"Members: {total_members}",
        f"Message: {guild_message_count}",
        "ztxhosting.site"
    ]

    current_status = statuses[status_index % len(statuses)]
    await bot.change_presence(activity=discord.Game(name=current_status))
    status_index += 1

# === Flask Keep-Alive Server ===
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Ticket Bot is Online!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# === Start Bot ===
keep_alive()
bot.run(TOKEN)
