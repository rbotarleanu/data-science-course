
import scrapy
import json


class ImobiliareSpider(scrapy.Spider):
	name = 'ImobiliareSpiderDetalii'
	output_file = 'pagini_detalii.txt'
	n_crawled_pages = 134
	# start_urls = ['https://www.imobiliare.ro/vanzare-apartamente/bucuresti']


	def start_requests(self):
		base_url = 'https://www.imobiliare.ro/vanzare-apartamente/bucuresti'
		
		yield scrapy.Request(url=base_url, callback=self.parse)
		
		for page_id in range(2, self.n_crawled_pages + 1):
			yield scrapy.Request(url='%s?pagina=%d' % (base_url, page_id),
								 callback=self.parse)

	def parse(self, response):
		print('\n\nParsing: %s' % response.url)
		detalii = response.xpath('''//h2[contains(@class, 'titlu-anunt hidden-xs')]/a/@href''').extract()
		preturi = response.xpath('''//div[contains(@class, 'box-pret-mobile')]''')

		if len(detalii) != len(preturi):
			print('\tFailed to parse!. Could not match postings.')
			return
		

		with open(self.output_file, 'a') as fout:
			for detaliu, pret in zip(detalii, preturi):
				price_v, currency_v, comission_v = self._extract_price_data(preturi)
				fout.write(json.dumps([detaliu, price_v, currency_v, comission_v]) + '\n')

	def _extract_price_data(self, price_selector):
		try:
			comision = price_selector.xpath('''./div[contains(@class, 'comision')]/text()''').extract()[0]
		except:
			comision = ''

		try:
			pret = price_selector.xpath('''.//span[contains(@class, 'pret-mare')]/text()''').extract()[0]
		except:
			pret = ''

		try:
			currency = price_selector.xpath('''.//span[contains(@itemprop, 'priceCurrency')]/text()''').extract()[0]
		except:
			currency = ''

		return pret, currency, comision