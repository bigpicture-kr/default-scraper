import json
import base64
import argparse
from urllib import parse
#from .dataclasses import *

class InstagramHarParser:
    def __init__(self, har_file, keyword):
        with open(har_file, "r") as file:
            data = json.loads(file.read())
        self.data = data['log']
        self.keyword = keyword
        self.contents = None

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

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--har_file",
        type=str,
        default="./data/www.instagram.com.har",
        help="The path of .har file containing the network log of the page to parse.",
    )
    arg_parser.add_argument(
        "--keyword",
        type=str,
        required=True,
        help="Search keyword for which to collect data.",
    )
    arg_parser.add_argument(
        "--output_file",
        type=str,
        default=None,
        help="The path to save processed file.",
    )

    args = arg_parser.parse_args()

    parser = InstagramHarParser(args.har_file, args.keyword)
    media_length = len(parser.get_media(args.output_file))
    print(f"{media_length} media found.")
