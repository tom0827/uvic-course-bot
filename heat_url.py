from constants import HEAT_BASE_URL, TermEnum

class HeatUrl():
    def __init__(self, course: str, term: str, year: str):
        self.url = None
        self.course = course.upper()
        self.term = TermEnum[term.upper()].value
        self.year = year

    def get_link(self):
        self.url = HEAT_BASE_URL.replace("<TERM>", self.year+self.term).replace("<COURSE>", self.course)
        return self.url
    
    def __valid_fields(self):
        if self.term not in TermEnum.__members__:
            error = f"Invalid term: {self.term}. Valid terms are {', '.join(TermEnum.__members__.keys())}."
            self.term = TermEnum[self.term].value
            return False, error
        return True, None