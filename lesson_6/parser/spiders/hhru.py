import scrapy
from scrapy.http  import HtmlResponse
from scrapy.http import HtmlResponse
from parser.items import ParserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&text=Python&from=suggest_post',
                  'https://spb.hh.ru/search/vacancy?area=231&search_field=name&search_field=company_name&search_field=description&text=Python&from=suggest_post']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        print(response);
        name_value = response.css('h1::text').get()
        salary_value = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url_value = response.url
        id_value = url_value
        yield ParserItem(name=name_value, salary=salary_value, url=url_value, _id=id_value,
                         salary_min=None, salary_max=None)


