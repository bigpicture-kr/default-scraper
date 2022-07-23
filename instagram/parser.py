import json
import base64
from urllib import parse

class InstagramHarParser:
    def __init__(self, har_file, keyword):
        with open(har_file, "r") as file:
            data = json.loads(file.read())
        self.data = data['log']
        self.keyword = keyword
    
    def parse_contents(self):
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
        return contents

if __name__ == "__main__":
    parser = InstagramHarParser("./data/www.instagram.com.har", "거꾸로먹는야쿠르트")
    parser.parse_contents()
