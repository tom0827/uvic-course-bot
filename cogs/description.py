import discord
from discord.ext import commands
from discord import app_commands
from constants import FOOTER_TEXT
from utils.course_info import CourseInfo
from utils.decorators import log_command, time_command
from logger import logger

class DescriptionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="description",
        description="Course description"
    )
    @app_commands.describe(
        department="Enter the course department (e.g., ECE, CSC)",
        course_number="Enter the course number (e.g., 471, 320)",
    )
    @log_command
    @time_command
    async def description(self, interaction: discord.Interaction, department: str, course_number: str):
        await interaction.response.defer()

        try:
            course_info = CourseInfo(department, course_number)
            course_info.get_info()

            # Check if course description exists
            if not course_info.description:
                logger.info(f"No description found for {department} {course_number}.")
                raise LookupError(f"No description found for {department.upper()} {course_number.upper()}.")

            embed = discord.Embed(
                title=f"{department.upper()} {course_number.upper()}",
                timestamp=discord.utils.utcnow(),
                color=discord.Color.blue()
            )
            
            embed.add_field(name="Description", value=course_info.description, inline=False)
            embed.set_footer(text=FOOTER_TEXT)
            
            await interaction.followup.send(embed=embed)

        except LookupError as le:
            logger.info(f"LookupError: {le}")
            await interaction.followup.send(f"⚠️ {le}", ephemeral=True)

async def setup(bot):
    import os
    APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "development").lower()

    if APP_ENVIRONMENT == "production":
        await bot.add_cog(DescriptionCog(bot))
        return

    guild_id_str = os.getenv("GUILD_IDS")
    ids = [int(guild_id.strip()) for guild_id in guild_id_str.split(",")]
    guild_objects = [discord.Object(id=guild_id) for guild_id in ids]
    await bot.add_cog(DescriptionCog(bot), guilds=guild_objects)