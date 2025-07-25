import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread

# === Settings ===
TOKEN = "MTM4MTMyODM2MzA1MzkxMjA3NA.Gbb0Kp.y96-QuBnYqIdMvWBz7_0VSAIGFcykYdS7_PFPs"  # Replace with your actual bot token
TICKET_CATEGORY_NAME = "🎫 Tickets"

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

message_count = 0
status_index = 0

# === Bot Events ===
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    update_status.start()

@bot.event
async def on_message(message):
    global message_count
    if not message.author.bot:
        message_count += 1
    await bot.process_commands(message)

# === Status Update Task ===
@tasks.loop(seconds=5)
async def update_status():
    global status_index

    total_members = sum(g.member_count for g in bot.guilds)
    total_servers = len(bot.guilds)
    total_tickets = 0

    for guild in bot.guilds:
        for category in guild.categories:
            if category.name == TICKET_CATEGORY_NAME:
                total_tickets += len(category.channels)

    statuses = [
        f"🎫 Tickets: {total_tickets}",
        f"👥 Members: {total_members}",
        f"💬 Messages: {message_count}",
        f"🏠 Servers: {total_servers}",
        "🤖 Powered by ZTX Hosting"
    ]

    current_status = statuses[status_index % len(statuses)]
    await bot.change_presence(activity=discord.Game(name=current_status))
    status_index += 1

# === Flask Keep-Alive Server ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Ticket Bot is Online!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# === Start Bot ===
keep_alive()
bot.run(TOKEN)