import json
import pandas as pd
import traceback
import requests
from .signin import signin
from .dto import *

class InstagramParser:
    def __init__(self, username, password, keyword, extract_all=False):
        self.username = username
        self.password = password
        self.keyword = keyword
        self.extract_all = extract_all
        self.cookies = None
        self.contents = None
        self.headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ko,en;q=0.9,en-US;q=0.8",
            "access-control-expose-headers": "X-IG-Set-WWW-Claim",
            "x-ig-app-id": "936619743392459",
        }

    def run(self, output_file=None):
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

        page, max_id = 1, ""
        print(f"Loading `section_info`...")
        try:
            while True:
                section_info = self.request_section_info(page, max_id)
                media_list += self.parse_sections(section_info)
                print(f"`section_info`[{page}] loaded.")

                if section_info['more_available']:
                    page = section_info['next_page']
                    max_id = section_info['next_max_id']
                else:
                    break
        except Exception:
            traceback.print_exc()
            pass
        print("All `section_info` loaded.")

        if output_file is not None:
            if output_file[-4:].lower() == ".csv":
                # Save as csv
                df = pd.DataFrame(media_list)
                df.to_csv(output_file)
            else:
                # Save as json
                with open(output_file, "w") as file:
                    string = json.dumps(media_list)
                    file.write(string)
            print(f"Data saved in `{output_file}`.")

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
    
    def request_section_info(self, page, max_id):
        response = requests.post(
            url=f"https://i.instagram.com/api/v1/tags/{self.keyword}/sections/",
            headers=self.headers,
            cookies=self.cookies,
            data={
                "page": page,
                "max_id": max_id,
                "include_persistent": 0,
                "surface": "grid",
                "tab": "recent",
            },
        )

        try:
            section_info = response.json()
        except Exception:
            print(response.status_code, response.content)
            raise Exception("Failed to load `section_info`.")
        
        return section_info

    def parse_sections(self, contents):
        contents = self.parse_sections_as_dict(contents)

        if self.extract_all:
            return contents
        
        contents_data = [InstagramContent(content).to_dict() for content in contents]

        return contents_data

    def parse_sections_as_dict(self, contents):
        section_medias = [
            content['layout_content']['medias']
            for content
            in contents['sections']
            if content['layout_type'] == "media_grid"
        ]

        contents_data = []
        for row_medias in section_medias:
            for media in row_medias:
                contents_data += media.values()

        return contents_data
    
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
