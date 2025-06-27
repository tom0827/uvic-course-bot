import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from logger import logger
from constants import FOOTER_TEXT
from utils.course_api_client import CourseApiClient
from utils.decorators import log_command, time_command
from utils.strings import format_prereqs, remove_html_tags

load_dotenv()
COURSE_API_URL = os.getenv("COURSE_API_URL")
client = CourseApiClient(COURSE_API_URL)

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
            data = client.get_course_info(course=f"{department}{course_number}")
            # Check if prerequisites or corequisites exist
            if not data.get("preAndCorequisites"):
                logger.error(f"No prerequisites or corequisites found for {department} {course_number}.")
                raise LookupError(f"No prerequisites or corequisites found for {department.upper()} {course_number.upper()}.")

            embed = discord.Embed(
                title=f"{department.upper()} {course_number.upper()}",
                timestamp=discord.utils.utcnow(),
                color=discord.Color.blue()
            )

            preAndCoReqs = format_prereqs(remove_html_tags(data.get("preAndCorequisites", "")))

            embed.add_field(name="Prerequisites", value=preAndCoReqs, inline=False)
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