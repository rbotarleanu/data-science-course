
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
				yield scrapy.Request(url=l['details'],
									 callback=partial(self.parse, main_page_info=l))

	def parse(self, response, main_page_info):
		print('\n\nParsing: %s' % response.url)

		detalii_complete = response.xpath('''//div[contains(@id, 'b_detalii_caracteristici')]/div/div/ul/li''')
		detalii_text = "\n".join(response.xpath('''//div[@id="b_detalii_text"]/p/text()''').extract())
		specificatii = "\n".join(response.xpath('''//div[@id="b_detalii_specificatii"]//text()''').extract())
		locatii = "\n".join(list(filter(lambda e: e != '', map(lambda d: d.strip(), response.xpath('''//div[@id="b-detalii-poi"]//text()''').extract()))))

		with open(self.output_file, 'a') as fout:
			features = self._get_features(detalii_complete)
			fout.write(json.dumps({
				**main_page_info,
				**features,
				"description": detalii_text,
				"specifications": specificatii,
				"poi": locatii
			}) + '\n')

	def _get_features(self, features_selector):
		d = {}
		for feature_selector in features_selector:
			feature = feature_selector.xpath('text()').extract()[0]
			value = feature_selector.xpath('./span/text()').extract()[0]
			d[feature] = value
		return d