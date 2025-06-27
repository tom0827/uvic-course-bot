import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from logger import logger
from constants import FOOTER_TEXT, HeatTermEnum
from utils.course_api_client import CourseApiClient
from utils.decorators import log_command, time_command

load_dotenv()
COURSE_API_URL = os.getenv("COURSE_API_URL")
client = CourseApiClient(COURSE_API_URL)

class HeatOutlineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="outline",
        description="Get heat outline for course"
    )
    @app_commands.describe(
        department="Enter the course department (e.g., ECE, CSC)",
        course_number="Enter the course number (e.g., 471, 320)",
        term="Enter term (Fall, Spring, Summer)",
        year="Enter year (e.g. 2025)"
    )
    @app_commands.choices(
        term=[
            app_commands.Choice(name="Fall", value="091"),
            app_commands.Choice(name="Spring", value="011"),
            app_commands.Choice(name="Summer", value="051")
        ],
        year=[
            app_commands.Choice(name="2023", value="2023"),
            app_commands.Choice(name="2024", value="2024"),
            app_commands.Choice(name="2025", value="2025"),
            app_commands.Choice(name="2026", value="2026"),
        ]
    )
    @log_command
    @time_command
    async def outline(
        self,
        interaction: discord.Interaction,
        department: str,
        course_number: str,
        term: str,
        year: str
    ):
        await interaction.response.defer()

        data = client.get_course_outline(term=f"{year}{term}", course=f"{department}{course_number}")

        if data.get('isValid') is False:
            data = client.get_course_outline(term=f"{year}{term}", course=f"{department}{course_number}", unpublished=True)
        
        if data.get('isValid') is False:
            await interaction.followup.send("⚠️ No valid outline found for the specified course.")
            return

        embed = discord.Embed(
            title=f"{department} {course_number} - {year} {self.get_term_name(term)}",
            timestamp=discord.utils.utcnow(),
            color=discord.Color.blue()
        )
        
        link = data.get("link")

        embed.add_field(name="Link", value=link, inline=False)
        embed.set_footer(text=FOOTER_TEXT)
        
        await interaction.followup.send(embed=embed)

    def get_term_name(self, term):
        if term == HeatTermEnum.SPRING.value:
            return "Spring"
        elif term == HeatTermEnum.FALL.value:
            return "Fall"
        elif term == HeatTermEnum.SUMMER.value:
            return "Summer"
        else:
            return "Unknown"

async def setup(bot):
    import os
    APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "development").lower()

    if APP_ENVIRONMENT == "production":
        await bot.add_cog(HeatOutlineCog(bot))
        return

    guild_id_str = os.getenv("GUILD_IDS")
    ids = [int(guild_id.strip()) for guild_id in guild_id_str.split(",")]
    guild_objects = [discord.Object(id=guild_id) for guild_id in ids]
    await bot.add_cog(HeatOutlineCog(bot), guilds=guild_objects)