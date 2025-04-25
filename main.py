import discord
from discord.ext import commands
from discord import app_commands

from course_availability import CourseAvailability
from course_info import CourseInfo
from heat_url import HeatUrl

import os
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(
        name="info",
        description="Basic course info",
        guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(course="Enter the course code (e.g., ECE471, CSC320)")
async def info(interaction: discord.Interaction, course: str):
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

@bot.tree.command(
        name="heat",
        description="Get heat outline for course",
        guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(
    course="Enter the course code (e.g., ECE471, CSC320)",
    term="Enter term (Fall, Spring, Summer)",
    year="Enter year (e.g. 2025)"
)
async def heat(interaction: discord.Interaction, course: str, term: str, year: str):
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


@bot.tree.command(
        name="availability",
        description="Find course availability",
        guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(
    subject="Enter the course subject (e.g., ECE, CSC)",
    course_number="Enter the course number (e.g., 471, 320)",
    term="Enter term (Fall, Spring, Summer)",
    year="Enter year (e.g. 2025)"
)
async def availability(
    interaction: discord.Interaction,
    subject: str,
    course_number: str,
    term: str,
    year: str
    ):
    await interaction.response.defer()

    course_availability = CourseAvailability(subject, course_number, term, year)
    data = await course_availability.get_availability()

    title = f"Availability for {subject} {course_number} - {data[0]['title']}"

    embed = discord.Embed(
        title=title,
        description=f"Description for {subject} {course_number}",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.blue()
    )

    
    for course in data:
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

        embed.add_field(name=field_name, value=field_value, inline=True)
    
    await interaction.followup.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

bot.run(os.getenv("TOKEN"))
