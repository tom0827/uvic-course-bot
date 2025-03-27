import discord
from discord.ext import commands
from discord import app_commands

from course_info import CourseInfo
from heat_url import HeatUrl

import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(
        name="info",
        description="Basic course info",
        guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(course="Enter the course code (e.g., ECE471, CSC320)")
async def info(interaction: discord.Interaction, course: str):
    course_info = CourseInfo(course)
    course_info.get_info()
    await interaction.response.send_message(
        f"Course info for: {course}\n\n"
        f"Title: {course_info.title}\n\n"
        f"Description: {course_info.description}\n\n"
        f"Prerequisites and Corequisites: {course_info.pre_and_co_reqs}"
    )

@bot.tree.command(
        name="heat",
        description="Get heat outline for course",
        guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(
    course="Enter the course code (e.g., ECE471, CSC320)",
    term="Enter term (Fall, Spring, Summer)",
    year="Enter year (e.g. 2025)"
)
async def heat(interaction: discord.Interaction, course: str, term: str, year: str):
    heat_url = HeatUrl(course, term, year)
    await interaction.response.send_message(heat_url.get_link())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

bot.run(os.getenv("TOKEN"))
