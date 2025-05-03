import discord
from discord.ext import commands
from discord import app_commands
import os

from utils.course_availability import CourseAvailability

class AvailabilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = int(os.getenv("GUILD_ID"))

    @app_commands.command(
        name="availability",
        description="Find course availability"
    )
    @app_commands.describe(
        subject="Enter the course subject (e.g., ECE, CSC)",
        course_number="Enter the course number (e.g., 471, 320)",
        term="Enter term (Fall, Spring, Summer)",
        year="Enter year (e.g. 2025)"
    )
    async def availability(
        self,
        interaction: discord.Interaction,
        subject: str,
        course_number: str,
        term: str,
        year: str
        ):
        await interaction.response.defer()

        course_availability = CourseAvailability(subject, course_number, term, year)
        data = await course_availability.get_availability()

        embed = discord.Embed(
            title=f"Course Information for {subject} {course_number} - {data[0]['title']}",
            description=f"Description for {subject} {course_number}", # TODO: Add hyperlink to course description
            timestamp=discord.utils.utcnow(),
            color=discord.Color.blue()
        )

        for idx, course in enumerate(data):
            available_spots = course['section_status'].split(" ")[0]

            method_emoji = "💻" if course['instructional_method'] == "Fully Online" else "🧑‍🏫"
            availability_emoji = "✅" if int(available_spots) > 0 else "❌"

            field_name = f"{course['type']} - {course['section']} {" (FULL)" if int(available_spots) == 0 else ""}"

            field_value = (
                f"#️⃣ **CRN:** {course['crn']}\n"
                f"{availability_emoji} **Status:** {course['section_status']}\n"
                f"📍 **Campus:** {course['campus']}\n"
                f"{method_emoji} **Delivery:** {course['instructional_method']}\n"
                f"⌚ **Meeting Times:** {course['meeting_time']}\n"
            )

            # When index is odd (field 1, 3, 5, etc.), add a blank field to create a two-column layout
            if idx % 2 == 1:
                embed.add_field(name="\u200b", value="\u200b", inline=True)
            
            embed.add_field(name=field_name, value=field_value, inline=True)
        
        # Add two blank fields if the number of courses is odd to maintain the two-column layout
        if len(data) % 2 == 1:
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)

        link_field_value = (
            f"[Course Search Link]({course_availability.url})\n"
            # TODO: Add link to course calendar
            # TODO: Add link to HEAT outline
        )
        embed.add_field(name="Links", value=link_field_value, inline=False)
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AvailabilityCog(bot), guilds=[discord.Object(id=int(os.getenv("GUILD_ID")))])