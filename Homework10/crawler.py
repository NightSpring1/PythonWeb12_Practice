"""
A python script to get quotes and authors from https://quotes.toscrape.com using Scrapy framework.

Run <python main.py> to get 2 JSON files: authors.json, quotes.json

Authors .json format:
[{  "fullname": "<name>",
    "born_date": "<date>",
    "born_location": "<location>",
    "description": "<description>"},]

Quotes .json format:
[{  "tags": [<tag1>,<tag2>],
    "author": "<author>",
    "quote": "<quote>"},]
"""

import scrapy
import json
from itemadapter import ItemAdapter
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuoteSpiderPipeline(object):
    quotes = []
    authors = []
    def process_item(self, item, spider):  # noqa
        if isinstance(item, QuoteItem):
            quote_adapter = ItemAdapter(item)
            self.quotes.append({
                "tags": quote_adapter["tags"],
                "author": quote_adapter["author"],
                "quote": quote_adapter["quote"]})

        elif isinstance(item, AuthorItem):
            author_adapter = ItemAdapter(item)
            self.authors.append({
                "fullname": author_adapter["fullname"],
                "born_date": author_adapter["born_date"],
                "born_location": author_adapter["born_location"],
                "description": author_adapter["description"]})
        return item

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as file_quotes:
            json.dump(self.quotes, file_quotes, ensure_ascii=False, indent=4)
        with open('authors.json', 'w', encoding='utf-8') as file_authors:
            json.dump(self.authors, file_authors, ensure_ascii=False, indent=4)


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    custom_settings = {"ITEM_PIPELINES": {QuoteSpiderPipeline: 500}}
    start_urls = ["https://quotes.toscrape.com"]

    all_authors = set()

    def parse(self, response):  # noqa
        for quote in response.xpath("/html//div[@class='quote']"):
            self.all_authors.add(quote.xpath("span/a/@href").get())
            yield QuoteItem(tags=quote.xpath("div[@class='tags']/a/text()").extract(),
                            author=quote.xpath("span/small/text()").get(),
                            quote=quote.xpath("span[@class='text']/text()").get())
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
        else:
            for author in self.all_authors:
                yield response.follow(self.start_urls[0] + author, self.parse_additional_page)

    @staticmethod
    def parse_additional_page(response):
        author = response.xpath('/html//div[@class="author-details"]')
        return AuthorItem(fullname=author.xpath('h3[@class="author-title"]/text()').get().strip(),
                          born_date=author.xpath('p/span[@class="author-born-date"]/text()').get(),
                          born_location=author.xpath('p/span[@class="author-born-location"]/text()').get(),
                          description=author.xpath('div[@class="author-description"]/text()').get().strip())


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuoteSpider)
    process.start()
