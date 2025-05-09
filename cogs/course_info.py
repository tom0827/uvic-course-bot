import os
import logging
import discord
from discord.ext import commands
from discord import app_commands

from utils.course_info import CourseInfo

class CourseInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = int(os.getenv("GUILD_ID"))
        self.logger = logging.getLogger(__name__)

    @app_commands.command(
        name="info",
        description="Basic course info"
    )
    @app_commands.describe(
        department="Enter the course department (e.g., ECE, CSC)",
        course_number="Enter the course number (e.g., 471, 320)",
    )
    async def info(self, interaction: discord.Interaction, department: str, course_number: str):
        self.logger.info(f"Received course info command: {department} {course_number}")
        await interaction.response.defer()
        course_info = CourseInfo(department, course_number)
        course_info.get_info()

        embed = discord.Embed(
            title=f"Course Info ({department} {course_number})",
            description=course_info.title,
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Description", value=course_info.description, inline=False)
        embed.add_field(name="Prerequisites and Corequisites", value=course_info.pre_and_co_reqs, inline=False)
        
        embed.set_footer(text="Course Information System")
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CourseInfoCog(bot), guilds=[discord.Object(id=int(os.getenv("GUILD_ID")))])