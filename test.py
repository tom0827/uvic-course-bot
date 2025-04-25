from constants import COURSE_SEARCH_BASE
from course_availability import CourseAvailability
import asyncio
from playwright.sync_api import sync_playwright
import requests
import json
import time


def fetch_course_page():
    """Fetch course page and wait until it loads using Playwright."""
    
    url = COURSE_SEARCH_BASE.format(
        TERM="202501",
        SUBJECT="ECE",
        COURSE_NUMBER="455"
    )

    print(f"Fetching URL: {url}")
    data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use headless mode
        page = browser.new_page()

        page.goto(url, wait_until="commit")
        page.wait_for_selector("#table1")

        element = page.query_selector("text=Please search again")

        # No results found. TODO: Handle this case accordingly
        if element:
            print(f"No results found")
            return

        rows = page.query_selector_all("#table1 tbody tr")
      
        for row in rows:
            course_title = row.query_selector("td[data-property='courseTitle'] a")
            subject = row.query_selector("td[data-property='subject']")
            course_number = row.query_selector("td[data-property='courseNumber']")
            section = row.query_selector("td[data-property='sequenceNumber']")
            schedule_type = row.query_selector("td[data-property='scheduleType']")
            credit_hours = row.query_selector("td[data-property='creditHours']")
            crn = row.query_selector("td[data-property='courseReferenceNumber']")
            campus = row.query_selector("td[data-property='campus']")
            instructional_method = row.query_selector("td[data-property='instructionalMethod']")
            meeting_time = row.query_selector("td[data-property='meetingTime']")
            section_status = row.query_selector("td[data-property='status']")
            
            # Extract text content from the elements
            course_title_text = course_title.inner_text() if course_title else "N/A"
            subject_text = subject.inner_text() if subject else "N/A"
            course_number_text = course_number.inner_text() if course_number else "N/A"
            section_text = section.inner_text() if section else "N/A"
            schedule_type_text = schedule_type.inner_text() if schedule_type else "N/A"
            credit_hours_text = credit_hours.inner_text() if credit_hours else "N/A"
            crn_text = crn.inner_text() if crn else "N/A"
            campus_text = campus.inner_text() if campus else "N/A"
            instructional_method_text = instructional_method.inner_text() if instructional_method else "N/A"
            meeting_time_text = meeting_time.inner_text() if meeting_time else "N/A"
            section_status_text = section_status.inner_text() if section_status else "N/A"
            
            # Store the extracted data in a dictionary
            data.append({
                "title": course_title_text,
                "subject": subject_text,
                "number": course_number_text,
                "section": section_text,
                "type": schedule_type_text,
                "crn": int(crn_text),
                "campus": campus_text,
                "instructional_method": instructional_method_text,
                "meeting_time": meeting_time_text,
                "section_status": section_status_text,
            })

        with open('courses_data.json', 'w') as f:
            json.dump(data, f, indent=4)

        browser.close()

start_time = time.time()
fetch_course_page()
end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")