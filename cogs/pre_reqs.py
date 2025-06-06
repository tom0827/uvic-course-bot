import discord
from discord.ext import commands
from discord import app_commands
from logger import logger
from constants import FOOTER_TEXT
from utils.course_info import CourseInfo
from utils.decorators import log_command, time_command

class PreReqsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="prereqs",
        description="Course prerequisites and corequisites"
    )
    @app_commands.describe(
        department="Enter the course department (e.g., ECE, CSC)",
        course_number="Enter the course number (e.g., 471, 320)",
    )
    @log_command
    @time_command
    async def prereqs(self, interaction: discord.Interaction, department: str, course_number: str):
        await interaction.response.defer()

        try:
            course_info = CourseInfo(department, course_number)
            course_info.get_info()

            # Check if prerequisites or corequisites exist
            if not course_info.pre_and_co_reqs:
                logger.error(f"No prerequisites or corequisites found for {department} {course_number}.")
                raise LookupError(f"No prerequisites or corequisites found for {department.upper()} {course_number.upper()}.")

            embed = discord.Embed(
                title=f"{department.upper()} {course_number.upper()}",
                timestamp=discord.utils.utcnow(),
                color=discord.Color.blue()
            )
            
            embed.add_field(name="Prerequisites", value=course_info.pre_and_co_reqs, inline=False)
            embed.set_footer(text=FOOTER_TEXT)
            
            await interaction.followup.send(embed=embed)
    
        except LookupError as le:
            logger.error(f"LookupError: {le}")
            await interaction.followup.send(f"⚠️ {le}", ephemeral=True)

async def setup(bot):
    import os
    APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "development").lower()

    if APP_ENVIRONMENT == "production":
        await bot.add_cog(PreReqsCog(bot))
        return

    guild_id_str = os.getenv("GUILD_IDS")
    ids = [int(guild_id.strip()) for guild_id in guild_id_str.split(",")]
    guild_objects = [discord.Object(id=guild_id) for guild_id in ids]
    await bot.add_cog(PreReqsCog(bot), guilds=guild_objects)