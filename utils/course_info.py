import requests

from constants import CATALOG_URL, DETAILS_BASE_URL

class CourseInfo():
    """Class to get basic course info"""
    def __init__(self, department: str, course_number: str):
        self.department = department.upper()
        self.course_number = course_number
        self.course = f"{self.department}{self.course_number}"
        self.title = None
        self.pid = None
        self.description = None
        self.pre_and_co_reqs = None

    def get_info(self):
        print("Getting course")
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

        details_response = requests.get(f"{DETAILS_BASE_URL}/{self.pid}")

        if details_response.status_code != 200:
            print("Error getting details")
            return

        details = details_response.json()
        self.description = self.__remove_html_tags(details.get('description'))
        self.pre_and_co_reqs = self.__remove_html_tags(details.get('preAndCorequisites'))
    
    def __remove_html_tags(self, text):
        from bs4 import BeautifulSoup
        return BeautifulSoup(text, "html.parser").get_text()

