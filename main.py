import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()
guild_id_str = os.getenv("GUILD_IDS")
GUILD_IDS = [int(guild_id.strip()) for guild_id in guild_id_str.split(",")]
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "development").lower()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs (command modules)
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f'Loaded cog: {filename}')

@bot.event
async def on_ready():
    logger.info(f'Bot is logged in as {bot.user.name} ({bot.user.id})')
    logger.info(f'APP_ENVIRONMENT: {APP_ENVIRONMENT}')
    if APP_ENVIRONMENT == "production":
        await bot.tree.sync()
        logger.info('Synced commands globally')
    else:
        logger.info('Syncing commands to specific guilds...')
        for guild_id in GUILD_IDS:
            await bot.tree.sync(guild=discord.Object(id=guild_id))
            logger.info(f'Synced commands to guild ID: {guild_id}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
