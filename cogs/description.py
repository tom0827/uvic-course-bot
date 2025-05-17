import os
import logging
import discord
from discord.ext import commands
from discord import app_commands

from constants import FOOTER_TEXT
from utils.course_info import CourseInfo

class DescriptionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @app_commands.command(
        name="description",
        description="Course description"
    )
    @app_commands.describe(
        department="Enter the course department (e.g., ECE, CSC)",
        course_number="Enter the course number (e.g., 471, 320)",
    )
    async def description(self, interaction: discord.Interaction, department: str, course_number: str):
        self.logger.info(f"Received description command: {department} {course_number}")
        await interaction.response.defer()
        course_info = CourseInfo(department, course_number)
        course_info.get_info()

        embed = discord.Embed(
            title=f"{department.upper()} {course_number.upper()}",
            timestamp=discord.utils.utcnow(),
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Description", value=course_info.description, inline=False)
        embed.set_footer(text=FOOTER_TEXT)
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    guild_id_str = os.getenv("GUILD_IDS")
    ids = [int(guild_id.strip()) for guild_id in guild_id_str.split(",")]
    guild_objects = [discord.Object(id=guild_id) for guild_id in ids]
    await bot.add_cog(DescriptionCog(bot), guilds=guild_objects)