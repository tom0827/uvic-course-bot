from constants import HEAT_BASE_URL, HeatTermEnum

class HeatUrl():
    def __init__(self, course: str, term: str, year: str):
        self.course = course.upper()
        self.term = term
        self.year = year
        # validate fields
        is_valid, error = self.__validate_fields()
        self.is_valid = is_valid
        self.error = error
        

    def get_link(self):
        return HEAT_BASE_URL.replace("<TERM>", self.year+self.term).replace("<COURSE>", self.course)
    
    def __validate_fields(self):
        if self.term.upper() not in HeatTermEnum.__members__:
            error = f"Invalid term: {self.term}."
            return False, error
        else:
            self.term = HeatTermEnum[self.term.upper()].value
        return True, None