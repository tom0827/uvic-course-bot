import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import datetime

load_dotenv()
guild_id_str = os.getenv("GUILD_IDS")
GUILD_IDS = [int(guild_id.strip()) for guild_id in guild_id_str.split(",")]
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

def setup_logging():
    # Create logs directory if it doesn't exist
    if not os.path.exists('./logs'):
        os.makedirs('./logs')
        
    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create a formatter with timestamp, level, and message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # File handler for all logs
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(f'./logs/discord_{current_date}.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Console handler for INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
logger = setup_logging()

# Load cogs (command modules)
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f'Loaded cog: {filename}')

@bot.event
async def on_ready():
    logger.info(f'Bot is logged in as {bot.user.name} ({bot.user.id})')
    for guild_id in GUILD_IDS:
        await bot.tree.sync(guild=discord.Object(id=guild_id))
        logger.info(f'Synced commands to guild ID: {guild_id}')

# Run the bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
