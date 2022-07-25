import json
import base64
import requests
from urllib import parse
#from .dataclasses import *

class InstagramHarParser:
    def __init__(self, har_file, keyword):
        with open(har_file, "r") as file:
            data = json.loads(file.read())
        self.data = data['log']
        self.keyword = keyword
        self.contents = None
        self.headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ko,en;q=0.9,en-US;q=0.8",
            "access-control-expose-headers": "X-IG-Set-WWW-Claim",
            "x-ig-app-id": "936619743392459",
        }

    def request_web_info(self):
        response = requests.get(
            url="https://i.instagram.com/api/v1/tags/web_info/",
            params={"tag_name": self.keyword},
            headers=self.headers,
        )
        return response.json()

    def get_media(self, output_file=None):
        if self.contents is None:
            self.parse_contents()
        
        media_list = []
        for content in self.contents:
            if "sections" not in content and "data" in content:
                # Instagram web_info API
                media_list += self.parse_sections(content['data']['top'])
                media_list += self.parse_sections(content['data']['recent'])
            elif "sections" in content:
                # Instagram sections API
                media_list += self.parse_sections(content)

        if output_file is not None:
            with open(output_file, "w") as file:
                string = json.dumps(media_list)
                file.write(string)
        
        return media_list

    def parse_sections(self, content_data):
        section_medias = [
            content['layout_content']['medias']
            for content
            in content_data['sections']
        ]

        media_list = []
        for row_medias in section_medias:
            for media in row_medias:
                media_list += media.values()

        return media_list
    
    def parse_contents(self, output_file=None):
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

        if output_file is not None:
            with open(output_file, "w") as file:
                string = json.dumps(contents)
                file.write(string)
        
        if len(contents) == 0:
            raise Exception("No instagram content was found in the input har file!")

        self.contents = contents
        return contents
