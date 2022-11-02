import scrapy
import pandas as pd
from scrapy.http import Response

from crawler.helpers.sitetypes import SiteType
from crawler.helpers.url import get_url_params, override_url_params


class Bearspace(scrapy.Spider):
    name = 'bearspace.co.uk'
    allowed_domains = ['bearspace.co.uk']
    site_type = SiteType.DEALER

    start_urls = [
        'https://www.bearspace.co.uk/purchase?page=1'
    ]

    def parse(self, response: Response, **kwargs):
        paintings_urls = response.xpath("//div[contains(@data-hook,'product')]/a/@href").getall()
        yield from response.follow_all(urls=paintings_urls, callback=self.parse_painting, priority=1)

        if paintings_urls:
            current_page = int(get_url_params(response.url).get('page', 1))
            next_page_url = override_url_params(response.url, {'page': current_page + 1})
            yield response.follow(url=next_page_url, callback=self.parse)

    def parse_painting(self, response: Response):

        url = response.xpath("//link[contains(@rel,'canonical')]/@href").get()
        title = response.xpath("//h1[contains(@data-hook,'title')]/text()").get()
        media = response.xpath("//pre[contains(@data-hook,'description')]/p[1]/span/text()").get()
        height = response.xpath("//pre[contains(@data-hook,'description')]/p[2]/span/text()").re_first(r'^(\d+)')
        width = response.xpath("//pre[contains(@data-hook,'description')]/p[2]/span/text()").re_first(r'x(\d+)')
        price = response.xpath("//span[contains(@data-hook,'primary-price')]/text()").re_first(r'\£(\d+)')

        data = [[url, title, media, height, width, price]]

        df = pd.DataFrame(data, columns=['url', 'title', 'media', 'height', 'weight', 'price'])
        print(df)
