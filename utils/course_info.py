import requests
import logging

from constants import CATALOG_URL, COURSE_CALENDAR_BASE, DETAILS_BASE_URL

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
        catalog_response = requests.get(CATALOG_URL)

        if catalog_response.status_code != 200:
            print("Error getting catalog")
            return

        catalog = catalog_response.json()
        course_item = next((item for item in catalog if item.get('__catalogCourseId') == self.course), None)

        if course_item is None:
            print("Course not found")
            return

        self.pid = course_item.get('pid')
        self.title = course_item.get('title')
        self.logger.info(f"Fetching Course Details Link: {DETAILS_BASE_URL}/{self.pid}")
        details_response = requests.get(f"{DETAILS_BASE_URL}/{self.pid}")

        if details_response.status_code != 200:
            print("Error getting details")
            return

        details = details_response.json()

        self.description = self.__remove_html_tags(details.get('description'))
        self.pre_and_co_reqs = self.__remove_html_tags(details.get('preAndCorequisites'))
        self.pre_and_co_reqs = self.__format_prereqs(self.pre_and_co_reqs)

    def get_course_calendar_link(self):
        return COURSE_CALENDAR_BASE.format(PID=self.pid)
    
    def __remove_html_tags(self, text):
        from bs4 import BeautifulSoup
        return BeautifulSoup(text, "html.parser").get_text(separator=" ", strip=True)
    
    def __format_prereqs(self, prereqs):
        if prereqs is None:
            return "No prerequisites"
        
        prereqs = (
            prereqs
            .replace(")", ")\n")
            .replace(": ", ":\n")
            .replace("following", "following\n")
        )

        split_prereqs = prereqs.split("\n")
        self.logger.info(f"Formatted prereqs: {prereqs.split("\n")}")
        formatted_prereqs = []

        for line in split_prereqs:
            if not len(line):
                continue

            self.logger.info(f"Line: {line}")

            count = sum(1 for char in line if char.isdigit())

            self.logger.info(f"Count: {count}")

            if count > 1:
                formatted_prereqs.append("- " + line.strip())
            else:
                formatted_prereqs.append(line.strip())

        self.logger.info(formatted_prereqs)

        formatted_prereqs = "\n".join(formatted_prereqs)

        return formatted_prereqs

