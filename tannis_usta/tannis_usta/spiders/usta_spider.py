import scrapy


class UstaSpider(scrapy.Spider):
	name = 'usta'

	def __init__(self, link_id=None, tournament_id=None, *args, **kwargs):
		super(UstaSpider, self).__init__(self, *args, **kwargs)
		self.start_urls = [
			'http://tennislink.usta.com/Tournaments/TournamentHome/Tournament.aspx?T={}#&&s=8Results1'.format(link_id)
		]

	def parse(self, response):
		yield scrapy.FormRequest(response.url, formdata={
			'__EVENTTARGET':'ctl00$mainContent$lnkbutDates',
			'__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first()}, callback=self.parse_tabs)

	def parse_tabs(self, response):
		for tab in response.xpath('//*[@id="ctl00_mainContent_ControlTabs2_ddlEvents"]/option/@value').extract():
			yield scrapy.FormRequest(response.url, formdata={
				'__EVENTTARGET': 'ctl00$mainContent$lnkbutDates',
				'__VIEWSTATE': response.css(
					'input#__VIEWSTATE::attr(value)').extract_first(),
				'ctl00$mainContent$ControlTabs2$ddlEvents': tab
			}, callback=self.parse_games)

	def parse_games(self, response):
		for result in response.xpath('//*[@id="ctl00_mainContent_ControlTabs2_panHTML"]/table[1]/tr'):
			yield {
				'Round Legend': result.xpath('./td[1]/text()').extract_first(),
				'Players': result.xpath('./td[2]/text()').extract_first(),
				'Points': result.xpath('./td[3]/text()').extract_first(),
			}


