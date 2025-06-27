from dotenv import load_dotenv
import os

import requests


class CourseApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_course_info(self, pid=None, course=None):
        if not pid and not course:
            return None
        params = {}
        if pid:
            params["pid"] = pid
        if not pid:
            params["course"] = course
            
        res = requests.get(f"{self.base_url}/courses/info", params=params)
        
        if res.status_code != 200:
            return None
        
        data = res.json().get('data')
        return data
    
    def get_course_sections(self, term=None, course=None):
        if not term and not course:
            return None
        res = requests.get(f"{self.base_url}/courses/sections/{term}/{course}")

        if res.status_code != 200:
                return None
            
        data = res.json().get('data', []).get('data', [])
        return data
    
    def get_course_outline(self, term=None, course=None, unpublished=False):
        if not term and not course:
            return None
        
        params = {}
        if unpublished:
            params['unpublished'] = 'true'
        
        res = requests.get(f"{self.base_url}/outline/{term}/{course}", params=params)

        if res.status_code != 200:
                return None
            
        data = res.json().get('data', {})
        return data
