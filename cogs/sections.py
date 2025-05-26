import discord
from discord.ext import commands
from discord import app_commands
import os

from logger import logger
from utils.sections import Sections
from utils.course_info import CourseInfo
from constants import FOOTER_TEXT, DaysOfWeekEnum
from utils.decorators import log_command, time_command

class SectionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="sections",
        description="Find course sections"
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
            app_commands.Choice(name="2023", value="2023"),
            app_commands.Choice(name="2024", value="2024"),
            app_commands.Choice(name="2025", value="2025"),
        ]
    )
    @log_command
    @time_command
    async def sections(
        self,
        interaction: discord.Interaction,
        department: str,
        course_number: str,
        term: str,
        year: str
        ):
        await interaction.response.defer()

        try:
            course_sections = Sections(department, course_number, term, year)
            res = course_sections.get_sections()
            data = res.get('data', [])

            if not data:
                logger.error(f"No sections found for {department} {course_number} in {term} {year}.")
                raise LookupError(f"No sections found for {department.upper()} {course_number.upper()} in {term} {year}.")

            course_info = CourseInfo(department, course_number)
            course_info.get_info()

            embed = self.create_embed(department, course_number, course_sections, data, course_info)
            await interaction.followup.send(embed=embed)

        except LookupError as le:
            logger.error(f"LookupError: {le}")
            await interaction.followup.send(f"⚠️ {le}", ephemeral=True)

    def create_embed(self, department, course_number, course_sections, data, course_info):
        embed = discord.Embed(
                title=f"Course Information for {department} {course_number} - {data[0]['courseTitle']}",
                timestamp=discord.utils.utcnow(),
                color=discord.Color.blue()
            )

        for idx, section in enumerate(data):
            self.add_section_field(embed, idx, section)
            
        # Add two blank fields if the number of courses is odd to maintain the two-column layout
        if len(data) % 2 == 1:
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)

        link_field_value = (
                f"[Course Search Link]({course_sections.url})\n"
                f"[Course Calendar Link]({course_info.get_course_calendar_link()})\n"
                # TODO: Add link to HEAT outline
            )
        embed.add_field(name="Links", value=link_field_value, inline=False)
        embed.set_footer(text=FOOTER_TEXT)
        return embed

    def add_section_field(self, embed, idx, section):
        available_spots = section['seatsAvailable']

        method_emoji = "💻" if section['instructionalMethodDescription'] == "Fully Online" else "🧑‍🏫"
        availability_emoji = "✅" if int(available_spots) > 0 else "❌"

        field_name = f"{section['scheduleTypeDescription']} - {section['sequenceNumber']} {" (FULL)" if int(available_spots) == 0 else ""}"

        section_data = section['meetingsFaculty'][0]['meetingTime']

        meeting_time_string = self.format_meeting_time_string(section, section_data)

        field_value = (
                    f"#️⃣ **CRN:** {section['courseReferenceNumber']}\n"
                    f"{availability_emoji} **Status:** {section['seatsAvailable']} seats available\n"
                    f"{method_emoji} **Delivery:** {section['instructionalMethodDescription']}\n"
                    f"📍 **Campus:** {section['campusDescription']}\n"
                    f"⌚ **Meeting Times:** {meeting_time_string}"
                    f"📅 **Duration** {section_data['startDate']} - "
                    f"{section_data['endDate']}\n"
                )

                # When index is odd (field 1, 3, 5, etc.), add a blank field to create a two-column layout
        if idx % 2 == 1:
            embed.add_field(name="\u200b", value="\u200b", inline=True)
                
        embed.add_field(name=field_name, value=field_value, inline=True)

    def format_meeting_time_string(self, section, section_data):
        meeting_time_string = f"{section_data['meetingTypeDescription']}\n"

        for s in section['meetingsFaculty']:
            meeting_time_data = s['meetingTime']
            days = ""
            for day in DaysOfWeekEnum:
                if meeting_time_data[day.name.lower()]:  # Convert enum name to lowercase to match dictionary keys
                    if len(days):
                        days += ", "
                    days += day.value
            if not days:
                continue
            meeting_time_string += days + ": "
            meeting_time_string += self.convert_to_12_hour_format(meeting_time_data['beginTime']) + " - "
            meeting_time_string += self.convert_to_12_hour_format(meeting_time_data['endTime']) + "\n"
        return meeting_time_string

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
    guild_id_str = os.getenv("GUILD_IDS")
    ids = [int(guild_id.strip()) for guild_id in guild_id_str.split(",")]
    guild_objects = [discord.Object(id=guild_id) for guild_id in ids]
    await bot.add_cog(SectionsCog(bot), guilds=guild_objects)