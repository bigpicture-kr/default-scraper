# default-scraper
Web Scraper

## Features

- Scrap all search results for a keyword entered as an argument.
- Can be saved as `.csv` and `.json`.
- Also collect user data who uploaded contents included in search results.

## Usage

### Install

```bash
pip install git+https://github.com/bigpicture-kr/default-scraper.git
```

It may require authentication before installing since default-scraper is a private repository of [bigpicture-kr](https://github.com/bigpicture-kr) organization.

### Scrap Instagram contents in python script

```python
from default_scraper.instagram.parser import InstagramParser
USERNAME = ""
PASSWORD = ""
KEYWORD = ""
parser = InstagramParser(USERNAME, PASSWORD, KEYWORD, False)
parser.run()
```

### Scrap Instagram contents using bash command

Run following command to scrap contents from Instagram:

```bash
python main.py --platform instagram --keyword {KEYWORD} [--output_file OUTPUT_FILE] [--all]
```

Use `--all` or `-a` option to also scrap unstructured fields.

## Data description

### Instagram

- Structured fields
  - `pk`
  - `id`
  - `taken_at`
  - `media_type`
  - `code`
  - `comment_count`
  - `user`
  - `like_count`
  - `caption`
  - `accessibility_caption`
  - `original_width`
  - `original_height`
  - `images`
- Some fields may be missing depending on Instagram's response data.

## Future works

- Will support scraping from more platform services.
