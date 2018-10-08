
import scrapy
import json
from functools import partial


class ImobiliareSpider(scrapy.Spider):
	name = 'ImobiliareSpiderDetalii'
	output_file = 'dataset.txt'
	n_crawled_pages = 134
	# start_urls = ['https://www.imobiliare.ro/vanzare-apartamente/bucuresti']

	def start_requests(self):
		with open('pagini_detalii.txt', 'rt') as fin:
			for line in fin:
				l = json.loads(line)
				yield scrapy.Request(url=l[0], callback=partial(self.parse, price_v=l[1], currency_v=l[2], comission_v=l[3]))

	def parse(self, response, price_v, currency_v, comission_v):
		print('\n\nParsing: %s' % response.url)
		print('Price_v:', price_v, 'currency:', 'currency_v', 'comision:', comission_v)
		detalii_complete = response.xpath('''//div[contains(@id, 'b_detalii_caracteristici')]/div/div/ul/li''')

		with open(self.output_file, 'a') as fout:
			features = self._get_features(detalii_complete)
			fout.write(json.dumps({
				'price': price_v,
				'currency': currency_v,
				'comission_v': comission_v,
				**features
			}) + '\n')

	def _get_features(self, features_selector):
		d = {}
		for feature_selector in features_selector:
			feature = feature_selector.xpath('text()').extract()[0]
			value = feature_selector.xpath('./span/text()').extract()[0]
			d[feature] = value
		return d