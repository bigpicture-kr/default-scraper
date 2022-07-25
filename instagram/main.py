import argparse
from config import *
from parser import InstagramParser

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    '''arg_parser.add_argument(
        "--har_file",
        type=str,
        default="./data/www.instagram.com.har",
        help="The path of .har file containing the network log of the page to parse.",
    )'''
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

    parser = InstagramParser(USERNAME, PASSWORD, args.keyword)
    data = parser.run()
    print(f"{len(data)} data found.")
