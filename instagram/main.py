import argparse
from .parser import InstagramHarParser

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
    data = parser.request_web_info()
    print(data)
    #media_length = len(parser.get_media(args.output_file))
    #print(f"{media_length} media found.")
