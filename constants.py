from enum import Enum

CATALOG_URL = 'https://uvic.kuali.co/api/v1/catalog/courses/5f21b66d95f09c001ac436a0'

DETAILS_BASE_URL = 'https://uvic.kuali.co/api/v1/catalog/course/5d9ccc4eab7506001ae4c225'

HEAT_BASE_URL = 'https://heat.csc.uvic.ca/coview/course/<TERM>/<COURSE>'

COURSE_SEARCH_BASE = (
    'https://banner.uvic.ca/StudentRegistrationSsb/ssb/classSearch/classSearch?'
    'term={TERM}&txt_subject={SUBJECT}&txt_courseNumber={COURSE_NUMBER}'
)

COURSE_CALENDAR_BASE = 'https://www.uvic.ca/calendar/undergrad/#/courses/{PID}'

class HeatTermEnum(Enum):
    FALL = "091"
    SPRING = "011"
    SUMMER = "051"

class CourseSearchTermEnum(Enum):
    FALL = "09"
    SPRING = "01"
    SUMMER = "05"