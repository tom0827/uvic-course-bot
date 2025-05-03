import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs (command modules)
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded extension: {filename[:-3]}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Command tree synced")

# Run the bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
