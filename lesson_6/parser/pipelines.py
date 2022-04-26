# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

class ParserPipeline:
    def __init__(self):
       client = MongoClient('127.0.0.1', 27017)
       self.db = client['db_hhru']
       self.vacancies = self.db.vac



    def process_item(self, item, spider):
        if spider.name == 'hh.ru':
            self.get_min_max_salery(item)
        #print(item)
        self.add_vac(item)
        return item

    def get_min_max_salery(self, item):
        item['salary_min'] = None
        item['salary_max'] = None
        sal = item['salary']
        for i in range(0, len(sal)):
            if sal[i].replace(" ", "") == 'от':
                item['salary_min'] = int(sal[i+1].replace("\xa0", ""))
            if sal[i].replace(" ", "") == 'до':
                item['salary_max'] = int(sal[i+1].replace("\xa0", ""))


    def add_vac(self, th_vac):
        try:
            self.vacancies.insert_one(th_vac)
            print('added')
        except DuplicateKeyError:
            print('Message is already exist')



