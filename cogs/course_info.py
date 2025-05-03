import os
import discord
from discord.ext import commands
from discord import app_commands

from utils.course_info import CourseInfo

class CourseInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = int(os.getenv("GUILD_ID"))

    @app_commands.command(
        name="info",
        description="Basic course info"
    )
    @app_commands.describe(course="Enter the course code (e.g., ECE471, CSC320)")
    async def info(self, interaction: discord.Interaction, course: str):
        course_info = CourseInfo(course)
        course_info.get_info()

        embed = discord.Embed(
            title=f"Course Info ({course})",
            description=course_info.title,
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Description", value=course_info.description, inline=False)
        embed.add_field(name="Prerequisites and Corequisites", value=course_info.pre_and_co_reqs, inline=False)
        
        embed.set_footer(text="Course Information System")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(CourseInfoCog(bot), guilds=[discord.Object(id=int(os.getenv("GUILD_ID")))])