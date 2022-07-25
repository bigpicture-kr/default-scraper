import json
import base64
import requests
from urllib import parse
from signin import signin
#from .dataclasses import *

class InstagramParser:
    def __init__(self, username, password, keyword):
        self.username = username
        self.password = password
        self.keyword = keyword
        self.cookies = None
        self.contents = None
        self.headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ko,en;q=0.9,en-US;q=0.8",
            "access-control-expose-headers": "X-IG-Set-WWW-Claim",
            "x-ig-app-id": "936619743392459",
        }

    def run(self):
        media_list = []

        # Sign-in and load cookies
        cookies = signin(self.username, self.password)
        self.cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        self.headers['x-csrftoken'] = self.cookies['csrftoken']
        print("Signed in.")

        # Request web_info, which is search result summary information
        print("Loading `web_info`...")
        web_info = self.request_web_info()
        media_list += self.parse_sections(web_info['top'])
        media_list += self.parse_sections(web_info['recent'])
        print("`web_info` loaded.")

        print("Loading `section_info`...")
        section_info = self.request_section_info()
        media_list += self.parse_sections(section_info)
        print("`section_info` loaded.")

        return media_list

    def request_web_info(self):
        response = requests.get(
            url="https://i.instagram.com/api/v1/tags/web_info/",
            params={"tag_name": self.keyword},
            headers=self.headers,
            cookies=self.cookies,
        )
        
        try:
            web_info = response.json()['data']
        except Exception:
            print(response.status_code, response.content)
            raise Exception("Failed to load `web_info`.")
        
        return web_info
    
    def request_section_info(self):
        response = requests.post(
            url=f"https://i.instagram.com/api/v1/tags/{self.keyword}/sections/",
            headers=self.headers,
            cookies=self.cookies,
        )

        try:
            section_info = response.json()
        except Exception:
            print(response.status_code, response.content)
            raise Exception("Failed to load `section_info`.")
        
        return section_info

    def parse_sections(self, content_data):
        section_medias = [
            content['layout_content']['medias']
            for content
            in content_data['sections']
            if content['layout_type'] == "media_grid"
        ]

        media_list = []
        for row_medias in section_medias:
            for media in row_medias:
                media_list += media.values()

        return media_list
    
    '''def parse_contents(self):
        prefixes = (
            "https://i.instagram.com/api/v1/tags/web_info/",
            f"https://i.instagram.com/api/v1/tags/{parse.quote(self.keyword)}/sections/",
        )
        contents = [
            json.loads(base64.b64decode(entry['response']['content']['text']).decode("utf-8"))
            for entry
            in self.data['entries']
            if entry['request']['method'] in ["GET", "POST"]
                and entry['request']['url'].startswith(prefixes)
                and 'text' in entry['response']['content'].keys()
        ]
        
        if len(contents) == 0:
            raise Exception("No instagram content was found in the input har file!")

        self.contents = contents
        return contents'''
