from enum import Enum

CATALOG_URL = 'https://uvic.kuali.co/api/v1/catalog/courses/5f21b66d95f09c001ac436a0'

DETAILS_BASE_URL = 'https://uvic.kuali.co/api/v1/catalog/course/67855445a0fe4e9a3f0baf82'

HEAT_BASE_URL = 'https://heat.csc.uvic.ca/coview/course/{TERM}/{COURSE}'

COURSE_SEARCH_BASE = (
    'https://banner.uvic.ca/StudentRegistrationSsb/ssb/classSearch/classSearch?'
    'term={TERM}&txt_subject={SUBJECT}&txt_courseNumber={COURSE_NUMBER}'
)

COURSE_CALENDAR_BASE = 'https://www.uvic.ca/calendar/undergrad/#/courses/{PID}'

COURSE_CALENDAR_BASE_KUALI = 'https://www.uvic.ca/calendar/undergrad/index.php#'

URL_PREFIX = "https://banner.uvic.ca/StudentRegistrationSsb/ssb"

COOKIE_LINK_BASE = '{PREFIX}/classSearch/classSearch?term={TERM}&txt_subject=CSUP&txt_courseNumber=000'

DATA_LINK_BASE = '{PREFIX}/searchResults/searchResults?txt_term={TERM}&pageMaxSize=10000&txt_subject={SUBJECT}&txt_courseNumber={COURSE_NUMBER}'

FOOTER_TEXT = (
    "UVic Course Information System"
)

class HeatTermEnum(Enum):
    SPRING = "011"
    FALL = "091"
    SUMMER = "051"

class DaysOfWeekEnum(Enum):
    SUNDAY = "S"
    MONDAY = "M"
    TUESDAY = "Tu"
    WEDNESDAY = "W"
    THURSDAY = "Th"
    FRIDAY = "F"
    SATURDAY = "S"
