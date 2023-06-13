# https://quotes.toscrape.com scraper

A python script to get quotes and authors from https://quotes.toscrape.com and saves them
into JSON format. Using Scrapy framework.

## Usage
Run **`python main.py`** to get 2 JSON files: authors.json, quotes.json


```text
Authors .json format:
[{  "fullname": "<name>",
    "born_date": "<date>",
    "born_location": "<location>",
    "description": "<description>"},]

Quotes .json format:
[{  "tags": [<tag1>,<tag2>],
    "author": "<author>",
    "quote": "<quote>"},]
```