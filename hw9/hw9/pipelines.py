# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from mongoengine import connect
from dotenv import load_dotenv
from itemadapter import ItemAdapter
from mongo_hw.models import Authors, Quotes
# pylint: disable=no-member



load_dotenv()
mongo_user = os.getenv('user')
mongodb_pass = os.getenv('pass')
db_name = os.getenv('db_name')
domain = os.getenv('domain')

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}"""
)


class QuotesSpiderPipeline:
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        author = Authors.objects(fullname=item['author']).first()
        if not author:
            author = Authors(
                fullname=item['author'],
            )
            author.save()
            print(f'Author {author.fullname} created.')
        else:
            print(f'Author {author.fullname} already exists.')

        author_name = item['author']
        author = Authors.objects(fullname=author_name).first()
        if author:
            quote = Quotes(
                quote=item['quote'],
                author=author,
                tags=item.get('tags', [])
            )
            quote.save()
            print(
                f'Quote "{quote.quote}" by {quote.author.fullname} saved.'
            )
        else:
            print(
                f'No author {author_name} for quote: {item["quote"]}.'
            )

        return item
