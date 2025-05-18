import discord
from discord.ext import commands
from discord import app_commands
import os
import logging

from constants import FOOTER_TEXT, HeatTermEnum
from utils.heat_outline import HeatUrl

class HeatOutlineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

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
            app_commands.Choice(name="2022", value="2022"),
            app_commands.Choice(name="2023", value="2023"),
            app_commands.Choice(name="2024", value="2024"),
            app_commands.Choice(name="2025", value="2025"),
        ]
    )
    async def outline(
        self,
        interaction: discord.Interaction,
        department: str,
        course_number: str,
        term: str,
        year: str
    ):
        self.logger.info(f"Received heat outline command: {department =} {course_number =} {term =} {year =}")
        await interaction.response.defer()
        heat_url = HeatUrl(department, course_number, term, year)
        
        embed = discord.Embed(
            title=f"Course Outline ({department} {course_number})",
            description=f"{department} {course_number} - {self.get_term_name(term)} {year}",
            timestamp=discord.utils.utcnow(),
            color=discord.Color.blue()
        )
        
        link = heat_url.get_link()
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
    guild_id_str = os.getenv("GUILD_IDS")
    ids = [int(guild_id.strip()) for guild_id in guild_id_str.split(",")]
    guild_objects = [discord.Object(id=guild_id) for guild_id in ids]
    await bot.add_cog(HeatOutlineCog(bot), guilds=guild_objects)