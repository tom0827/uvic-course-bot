import discord
from discord.ext import commands
from discord import app_commands
import os
import time
import logging

from utils.course_availability import CourseAvailability
from utils.course_info import CourseInfo

class AvailabilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = int(os.getenv("GUILD_ID"))
        self.logger = logging.getLogger(__name__)

    @app_commands.command(
        name="availability",
        description="Find course availability"
    )
    @app_commands.describe(
        department="Enter the course department (e.g., ECE, CSC)",
        course_number="Enter the course number (e.g., 471, 320)",
        term="Enter term (Fall, Spring, Summer)",
        year="Enter year (e.g. 2025)"
    )
    @app_commands.choices(
        term=[
            app_commands.Choice(name="Fall", value="09"),
            app_commands.Choice(name="Spring", value="01"),
            app_commands.Choice(name="Summer", value="05")
        ],
        year=[
            app_commands.Choice(name="2022", value="2022"),
            app_commands.Choice(name="2023", value="2023"),
            app_commands.Choice(name="2024", value="2024"),
            app_commands.Choice(name="2025", value="2025"),
        ]
    )
    async def availability(
        self,
        interaction: discord.Interaction,
        department: str,
        course_number: str,
        term: str,
        year: str
        ):
        self.logger.info(f"Received availability command: {department} {course_number} {term} {year}")
        start_time = time.time()
        await interaction.response.defer()

        course_availability = CourseAvailability(department, course_number, term, year)
        res = course_availability.get_availability()
        data = res['data']

        course_info = CourseInfo(department, course_number)
        course_info.get_info()

        embed = discord.Embed(
            title=f"Course Information for {department} {course_number} - {data[0]['courseTitle']}",
            description=course_info.description, # TODO: Add hyperlink to course description
            timestamp=discord.utils.utcnow(),
            color=discord.Color.blue()
        )

        for idx, section in enumerate(data):
            available_spots = section['seatsAvailable']

            method_emoji = "💻" if section['instructionalMethodDescription'] == "Fully Online" else "🧑‍🏫"
            availability_emoji = "✅" if int(available_spots) > 0 else "❌"

            field_name = f"{section['scheduleTypeDescription']} - {section['sequenceNumber']} {" (FULL)" if int(available_spots) == 0 else ""}"

            meeting_time_data = section['meetingsFaculty'][0]['meetingTime']

            days_of_week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            days = ""

            for day in days_of_week:
                if meeting_time_data[day]:
                    days += day.capitalize() + "\n"

            field_value = (
                f"#️⃣ **CRN:** {section['courseReferenceNumber']}\n"
                f"{availability_emoji} **Status:** {section['seatsAvailable']} seats available\n"
                f"{method_emoji} **Delivery:** {section['instructionalMethodDescription']}\n"
                f"📍 **Campus:** {section['campusDescription']}\n"
                f"⌚ **Meeting Times:** {meeting_time_data['meetingTypeDescription']}\n"
                f"{days}"
                f"{self.convert_to_12_hour_format(meeting_time_data['beginTime'])} - "
                f"{self.convert_to_12_hour_format(meeting_time_data['endTime'])}\n"
                f"📅 **Duration** {meeting_time_data['startDate']} - "
                f"{meeting_time_data['endDate']}\n"
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
            f"[Course Calendar Link]({course_info.get_course_calendar_link()})\n"
            # TODO: Add link to HEAT outline
        )
        embed.add_field(name="Links", value=link_field_value, inline=False)
        end_time = time.time()
        embed.set_footer(text=f"Response Time: {end_time - start_time:.2f} seconds")
        await interaction.followup.send(embed=embed)

    def convert_to_12_hour_format(self, time):
        if not time:
            return "N/A"
        
        time = time.strip()
        
        hours = int(time[:2])
        minutes = int(time[2:])
        
        # Determine AM or PM
        period = "AM" if hours < 12 else "PM"
        
        # Convert hours to 12-hour format
        if hours == 0:
            hours = 12
        elif hours > 12:
            hours -= 12
        
        return f"{hours}:{minutes:02d} {period}"

async def setup(bot):
    await bot.add_cog(AvailabilityCog(bot), guilds=[discord.Object(id=int(os.getenv("GUILD_ID")))])