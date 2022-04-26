import scrapy
from scrapy.http import HtmlResponse
from parser.items import ParserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://spb.superjob.ru/vacancy/search/']

    def parse(self, response):
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@class='f-test-search-result-item']//@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        print(response);
        name_value = response.css('h1::text').get()
        # salary_value = response.xpath("'//div/div/div/div/div/div/div/div/div/span/span[@class]']//text()").getall()
        # не удается написать xpath наименования все "запутаны"
        url_value = response.url
        id_value = url_value
        yield ParserItem(name=name_value, salary=None, url=url_value, _id=id_value,
                         salary_min=None, salary_max=None)

