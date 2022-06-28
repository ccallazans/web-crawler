# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmericanasItem(scrapy.Item):
    gtin = scrapy.Field()
    descricao = scrapy.Field()
    preco = scrapy.Field()
    url = scrapy.Field()
    url_photo = scrapy.Field()
