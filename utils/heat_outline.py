from constants import HEAT_BASE_URL

class HeatUrl():
    def __init__(self, department: str, course_number, term: str, year: str):
        self.department = department.upper()
        self.course_number = course_number
        self.course = f"{self.department}{self.course_number}"
        self.term = term
        self.year = year

    def get_link(self):
        return HEAT_BASE_URL.format(
            TERM=self.year+self.term,
            COURSE=self.course
        )
