import discord
from discord.ext import commands
from discord import app_commands
import os

from utils.heat_outline import HeatUrl

class HeatOutlineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = int(os.getenv("GUILD_ID"))

    @app_commands.command(
        name="heat",
        description="Get heat outline for course"
    )
    @app_commands.describe(
        course="Enter the course code (e.g., ECE471, CSC320)",
        term="Enter term (Fall, Spring, Summer)",
        year="Enter year (e.g. 2025)"
    )
    async def heat(self, interaction: discord.Interaction, course: str, term: str, year: str):
        heat_url = HeatUrl(course, term, year)
        if not heat_url.is_valid:
            await interaction.response.send_message(heat_url.error)
            return
        
        embed = discord.Embed(
            title=f"Course Outline ({course})",
            description=f"{course} - {term} {year}",
            color=discord.Color.blue()
        )
        
        link = heat_url.get_link()
        embed.add_field(name="Link", value=link, inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(HeatOutlineCog(bot), guilds=[discord.Object(id=int(os.getenv("GUILD_ID")))])