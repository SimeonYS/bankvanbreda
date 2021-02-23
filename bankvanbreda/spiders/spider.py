import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import BankvanbredaItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class BankvanbredaSpider(scrapy.Spider):
	name = 'bankvanbreda'
	start_urls = ['https://blog.bankvanbreda.be/']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class,"blog__post")]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="page-header__info"]/text()').get()
		if not date:
			date = "Date is not published"
		title = response.xpath('//h1/span[@id="hs_cos_wrapper_name"]/text()').get()
		content = response.xpath('//div[@class="blog-post-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=BankvanbredaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
