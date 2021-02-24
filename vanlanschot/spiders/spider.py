import scrapy

from scrapy.loader import ItemLoader
from ..items import VanlanschotItem
from itemloaders.processors import TakeFirst


class VanlanschotSpider(scrapy.Spider):
	name = 'vanlanschot'
	start_urls = ['https://www.vanlanschot.nl/inspiratie/ons-cultureel-en-maatschappelijk-vermogen']

	def parse(self, response):
		post_links = response.xpath('//a[@class="c-ticket__clickarea"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//nav[@class="c-nav-paging"]//div[contains(@class, "c-nav-paging__wrap-next")]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('(//div[contains(@class, "c-rte--intro")])[1]//text()[normalize-space()]|(//div[@class="c-rte  u-module  u-mb  "])[1]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="c-label  c-label__secondary-text has-separator"]/text()').get()

		item = ItemLoader(item=VanlanschotItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

	'//section//div[@class="c-rte  u-module  u-mb   u-text-light  u-epsilon  c-rte--intro"]'
