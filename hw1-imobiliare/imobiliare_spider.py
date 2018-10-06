
import scrapy
import json


class ImobiliareSpider(scrapy.Spider):
	name = 'ImobiliareSpider'
	output_file = 'date_imobiliare.txt'
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
		caracteristici = response.xpath('''//*[contains(@class, 'caracteristici')]''')
		preturi = response.xpath('''//div[contains(@class, 'box-pret-mobile')]''')
		titluri = response.xpath('''//h2[contains(@class, 'titlu-anunt hidden-xs')]/a/span/text()''')

		if len(caracteristici) != len(preturi) != len(titluri):
			print('\tFailed to parse!. Could not match postings.')
			return

		print('\tExtracting data...')
		data = self._extract_data(titluri, preturi, caracteristici)

	def _extract_data(self, titluri, preturi, caracteristici):
		data = []
		for titlu, pret, car in zip(titluri, preturi, caracteristici):
			try:
				entry = {}
				title_v = titlu.extract()
				price_v, currency_v, comission_v = self._extract_price_data(pret)
				characteristics_v = self._extract_characteristics(car)

				entry = {
					'title': title_v,
					'price': price_v,
					'currency': currency_v,
					'commision': comission_v,
					'characteristics': characteristics_v
				}
				with open(self.output_file, 'a') as fout:
					fout.write(json.dumps(entry) + '\n')
			except Exception as e:
				print(e)

	def _extract_characteristics(self, characteristics_selector):
		try:
			characteristics = characteristics_selector.xpath('./li/span/text()').extract()
		except:
			characteristics = []
		finally:
			return characteristics

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