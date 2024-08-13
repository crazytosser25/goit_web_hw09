import scrapy
from hw9.items import QuotesSpiderItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for i in response.xpath("//div[@class='quote']"):
            # print(i.xpath("span/small/text()").get())
            # print(i.xpath("span[@itemprop='text']/text()").get())
            # print(i.xpath('div[@class="tags"]/a[@class="tag"]/text()').getall())
            item = QuotesSpiderItem(
                author = i.xpath(
                    "span/small/text()"
                ).get(),

                quote = i.xpath(
                    "span[@itemprop='text']/text()"
                ).get().strip('“”'),

                tags = i.xpath(
                    'div[@class="tags"]/a[@class="tag"]/text()'
                ).getall()
            )
            yield item

        next_page = response.xpath("//a[contains(text(), 'Next')]/@href").get()
        # print(next_page)
        if next_page:
            yield scrapy.Request(
                url = self.start_urls[0] + next_page
            )
