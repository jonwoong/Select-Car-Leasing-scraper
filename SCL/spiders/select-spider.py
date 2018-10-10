import scrapy
from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join

class Offer(scrapy.Item):
	car = scrapy.Field()
	price = scrapy.Field()
	initial_payment = scrapy.Field()
	months_term = scrapy.Field()
	miles_per_annum = scrapy.Field()

class OfferLoader(ItemLoader):
	car_out = Join(" ")

class OfferSpider(scrapy.Spider):
	name = "select"

	start_urls = ['https://www.selectcarleasing.co.uk/all-special-offers.html']

	def parse(self, response):

		special_blocks = response.css('div.offer')

		for special in special_blocks:
			offerLoader = OfferLoader(item=Offer(),response=response)
			offerLoader.add_value('car', special.css('div.omake::text').extract_first()) 
			offerLoader.add_value('car', special.css('div::text')[1].extract())
			offerLoader.add_value('price', special.css('big::text')[2].extract().encode('utf-8'))
			months_miles_initial = special.css('small.tpnoshow.mobilenoshow::text')

			if len(months_miles_initial) == 4:
				offerLoader.add_value('months_term', special.css('small.tpnoshow.mobilenoshow::text')[2].extract().split(" ")[0])
				offerLoader.add_value('miles_per_annum', special.css('small.tpnoshow.mobilenoshow::text')[2].extract().split(" ")[3])
				offerLoader.add_value('initial_payment', special.css('small.tpnoshow.mobilenoshow::text')[3].extract().encode('utf-8').split(" ")[2] + " ex VAT")
			elif len(months_miles_initial) == 3:
				offerLoader.add_value('months_term', special.css('small.tpnoshow.mobilenoshow::text')[1].extract().split(" ")[0])
				offerLoader.add_value('miles_per_annum', special.css('small.tpnoshow.mobilenoshow::text')[1].extract().split(" ")[3])
				offerLoader.add_value('initial_payment', special.css('small.tpnoshow.mobilenoshow::text')[2].extract().encode('utf-8').split(" ")[2] + " ex VAT")

			yield offerLoader.load_item()


		# follow pagination links
		for href in response.xpath('//*[contains(@class,"previousnext pager")]'):
			yield response.follow(href, self.parse)