import json
import requests
from constants import COOKIE_LINK_BASE, COURSE_SEARCH_BASE, DATA_LINK_BASE, URL_PREFIX
from playwright.async_api import async_playwright

class Sections():
    def __init__(self, subject: str, course_number: str, term: str, year: str):
        self.subject = subject
        self.course_number = course_number
        self.term = term
        self.year = year
        self.url = COURSE_SEARCH_BASE.format(
            TERM=self.year+self.term,
            SUBJECT=self.subject,
            COURSE_NUMBER=self.course_number
        )

    def get_sections(self):
        cookie_link = COOKIE_LINK_BASE.format(
            PREFIX=URL_PREFIX,
            TERM=self.year+self.term
        )

        session = requests.Session()
        session.get(cookie_link)

        data_link = DATA_LINK_BASE.format(
            PREFIX=URL_PREFIX,
            TERM=self.year+self.term,
            SUBJECT=self.subject,
            COURSE_NUMBER=self.course_number
        )

        data_response = session.get(data_link)
        return json.loads(data_response.text)
