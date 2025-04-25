import requests
from constants import COURSE_SEARCH_BASE, CourseSearchTermEnum
from playwright.async_api import async_playwright
import json

class CourseAvailability():
    def __init__(self, subject: str, course_number: str, term: str, year: str):
        self.subject = subject
        self.course_number = course_number
        self.term = term
        self.year = year
        is_valid, error = self.__validate_fields()
        self.is_valid = is_valid
        self.error = error

    async def get_availability(self):
        url = COURSE_SEARCH_BASE.format(
            TERM=self.year+self.term,
            SUBJECT=self.subject,
            COURSE_NUMBER=self.course_number
        )
        print(f"Fetching URL: {url}")
    
        data = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)  # Use headless mode
            page = await browser.new_page()

            await page.goto(url, wait_until="commit")
            await page.wait_for_selector("#table1")

            element = await page.query_selector("text=Please search again")

            # TODO: Handle no data
            if element:
                print(f"No results found")
                return

            rows = await page.query_selector_all("#table1 tbody tr")
        
            for row in rows:
                course_title = await row.query_selector("td[data-property='courseTitle'] a")
                subject = await row.query_selector("td[data-property='subject']")
                course_number = await row.query_selector("td[data-property='courseNumber']")
                section = await row.query_selector("td[data-property='sequenceNumber']")
                schedule_type = await row.query_selector("td[data-property='scheduleType']")
                credit_hours = await row.query_selector("td[data-property='creditHours']")
                crn = await row.query_selector("td[data-property='courseReferenceNumber']")
                campus = await row.query_selector("td[data-property='campus']")
                instructional_method = await row.query_selector("td[data-property='instructionalMethod']")
                meeting_time = await row.query_selector("td[data-property='meetingTime']")
                section_status = await row.query_selector("td[data-property='status']")
                
                course_title_text = await course_title.inner_text() if course_title else "N/A"
                subject_text = await subject.inner_text() if subject else "N/A"
                course_number_text = await course_number.inner_text() if course_number else "N/A"
                section_text = await section.inner_text() if section else "N/A"
                schedule_type_text = await schedule_type.inner_text() if schedule_type else "N/A"
                credit_hours_text = await credit_hours.inner_text() if credit_hours else "N/A"
                crn_text = await crn.inner_text() if crn else "N/A"
                campus_text = await campus.inner_text() if campus else "N/A"
                instructional_method_text = await instructional_method.inner_text() if instructional_method else "N/A"
                meeting_time_text = await meeting_time.inner_text() if meeting_time else "N/A"
                section_status_text = await section_status.inner_text() if section_status else "N/A"

                week_pattern = "\nS\nM\nT\nW\nT\nF\nS\n"
                none_pattern = "\n -\n"

                meeting_time_text_list = meeting_time_text.replace(week_pattern, "\n").replace(none_pattern, "\n").split("\n")
                filtered_words = [word for word in meeting_time_text_list if "building" not in word.lower() and "room" not in word.lower()]
                meeting_time_text = "\n".join(filtered_words)
                
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
                    "section_status": section_status_text.replace("LINKED", "").replace("FULL:", "").rstrip("\n").replace("\n", "").strip(),
                    "credits": credit_hours_text,
                })

            with open('courses_data.json', 'w') as f:
                json.dump(data, f, indent=4)

            await browser.close()
        
        return data
        
    def __validate_fields(self):
        if self.term.upper() not in CourseSearchTermEnum.__members__:
            error = f"Invalid term: {self.term}."
            return False, error
        else:
            self.term = CourseSearchTermEnum[self.term.upper()].value
        return True, None