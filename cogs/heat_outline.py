import discord
from discord.ext import commands
from discord import app_commands
import os
import logging

from utils.heat_outline import HeatUrl

class HeatOutlineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = int(os.getenv("GUILD_ID"))
        self.logger = logging.getLogger(__name__)

    @app_commands.command(
        name="heat",
        description="Get heat outline for course"
    )
    @app_commands.describe(
        department="Enter the course department (e.g., ECE, CSC)",
        course_number="Enter the course number (e.g., 471, 320)",
        term="Enter term (Fall, Spring, Summer)",
        year="Enter year (e.g. 2025)"
    )
    async def heat(
        self,
        interaction: discord.Interaction,
        department: str,
        course_number: str,
        term: str,
        year: str
    ):
        self.logger.info(f"Received heat outline command: {department} {course_number} {term} {year}")
        await interaction.response.defer()
        heat_url = HeatUrl(department, course_number, term, year)
        if not heat_url.is_valid:
            await interaction.response.send_message(heat_url.error)
            return
        
        embed = discord.Embed(
            title=f"Course Outline ({department} {course_number})",
            description=f"{department} {course_number} - {term} {year}",
            color=discord.Color.blue()
        )
        
        link = heat_url.get_link()
        embed.add_field(name="Link", value=link, inline=False)
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HeatOutlineCog(bot), guilds=[discord.Object(id=int(os.getenv("GUILD_ID")))])