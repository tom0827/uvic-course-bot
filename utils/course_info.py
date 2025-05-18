import requests
import logging
from constants import CATALOG_URL, COURSE_CALENDAR_BASE, COURSE_CALENDAR_BASE_KUALI, DETAILS_BASE_URL
from bs4 import BeautifulSoup

class CourseInfo():
    """Class to get basic course info"""
    def __init__(self, department: str, course_number: str):
        self.logger = logging.getLogger(__name__)
        self.department = department.upper()
        self.course_number = course_number
        self.course = f"{self.department}{self.course_number}"
        self.title = None
        self.pid = None
        self.description = None
        self.pre_and_co_reqs = None

    def get_info(self):
        catalog_response = requests.get(CATALOG_URL, timeout=10)
        catalog_response.raise_for_status()

        catalog = catalog_response.json()
        course_item = next((item for item in catalog if item.get('__catalogCourseId') == self.course), None)

        if course_item is None:
            self.logger.warning(f"Course {self.course} not found in catalog.")
            return

        self.pid = course_item.get('pid')
        self.title = course_item.get('title')

        self.logger.info(f"Fetching Course Details Link: {DETAILS_BASE_URL}/{self.pid}")

        details_response = requests.get(f"{DETAILS_BASE_URL}/{self.pid}", timeout=10)
        details_response.raise_for_status()

        details = details_response.json()

        self.description = self.__remove_html_tags(details.get('description'))

        self.pre_and_co_reqs = self.__remove_html_tags(details.get('preAndCorequisites'))
        self.pre_and_co_reqs = self.__format_prereqs(self.pre_and_co_reqs)

    def get_course_calendar_link(self):
        if not self.pid:
            self.logger.error("PID is not set. Cannot generate course calendar link.")
            return

        return COURSE_CALENDAR_BASE.format(PID=self.pid)
    
    def __remove_html_tags(self, text):
        return BeautifulSoup(text, "html.parser").get_text(separator=" ", strip=True)
    
    def __format_prereqs(self, prereqs):
        if prereqs is None or not prereqs.strip():
            return "No prerequisites"
        
        prereqs = (
            prereqs
            .replace(")", ")\n")
            .replace(": ", ":\n")
            .replace("following", "following\n")
            .replace("Complete", "\nComplete")
        )

        split_prereqs = prereqs.split("\n")
        formatted_prereqs = []

        for line in split_prereqs:
            if not len(line):
                continue
            
            line = line.strip()
            count = sum(1 for char in line if char.isdigit())

            if count > 1:
                formatted_prereqs.append("- " + line.strip())
            else:
                formatted_prereqs.append(line.strip())

        formatted_prereqs = "\n".join(formatted_prereqs)
        return formatted_prereqs

