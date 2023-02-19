# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProducthuntReviewItem(scrapy.Item):
    # define the fields for your item here like:
    external_id = scrapy.Field()
    full_text = scrapy.Field()
    user_id = scrapy.Field()
    user_screen_name = scrapy.Field()
    profile_image_url = scrapy.Field()
