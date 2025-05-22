import subprocess

from constants import HEAT_BASE_URL
from logger import logger

class HeatUrl():
    def __init__(self, department: str, course_number, term: str, year: str):
        self.department = department.upper()
        self.course_number = course_number
        self.course = f"{self.department}{self.course_number}"
        self.term = term
        self.year = year
        self.published_link_valid = False
        self.unpublished_link_valid = False

    def get_link(self):

        published_link = HEAT_BASE_URL.format(
            TERM=self.year+self.term,
            COURSE=self.course
        )

        published_link_exists = self.check_link_exists(published_link)
        if published_link_exists:
            self.published_link_valid = True
            return published_link
        
        unpublished_link = published_link + "&unp=t"

        unpublished_link_exists = self.check_link_exists(unpublished_link)
        if unpublished_link_exists:
            self.unpublished_link_valid = True
            return unpublished_link


    def check_link_exists(self, url):
        logger.info(f"Checking link: {url}")

        curl_command = [
            "curl",
            "--cacert", "./server_cert.pem", #TODO: At some point this file will have to be regenerated
            url
        ]

        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if len(result.stdout) < 2000:
            return False

        return True

