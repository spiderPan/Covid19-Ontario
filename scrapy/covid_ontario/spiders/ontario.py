# -*- coding: utf-8 -*-
import scrapy
from covid_ontario.items import CovidOntarioStatusItem
from scrapy.utils.response import open_in_browser
import datetime


class OntarioSpider(scrapy.Spider):
    name = 'ontario'
    allowed_domains = ['www.ontario.ca']
    start_urls = [
        'https://www.ontario.ca/page/2019-novel-coronavirus'
    ]

    def parse(self, response):
        status_item = CovidOntarioStatusItem()
        status_dict = {
            'Number of cases': 'confirmed',
            'Resolved': 'resolved',
            'Deceased': 'deceased',
            'Investigation': 'pending',
            'Total': 'total',
            'Male': 'male',
            'Female': 'female',
            '19': 'youth',
            '20-64': 'adult',
            '65': 'senior',
        }
        # status_table = response.css('.field-type-text-with-summary table')[0]
        # self.logger.warning('Table HTML %s', response)
        # open_in_browser(response)
        daily_data = {}
        for row in response.xpath('//table[1]/tbody/tr'):
            name = row.xpath(
                'td[1]/descendant-or-self::*/text()').get().strip()
            value = row.xpath(
                'td[2]/descendant-or-self::*/text()').get().strip()
            for label, key in status_dict.items():
                if name and value and label in name:
                    value = int(value.replace(',', ''))
                    # self.logger.warning('Table Name %s', name)
                    # self.logger.warning('Label %s', label)
                    # self.logger.warning('Value %s', value)
                    daily_data[key] = value

        date_timestamp = datetime.datetime.now().strftime("%B %d, %Y")
        status_item['date'] = date_timestamp
        status_item['confirmed'] = {
            'total': daily_data['confirmed'],
            'male': daily_data['male'],
            'female': daily_data['female'],
            'youth': daily_data['youth'],
            'adult': daily_data['adult'],
            'senior': daily_data['senior'],
        }
        status_item['deceased'] = daily_data['deceased']
        status_item['pending'] = daily_data['pending']
        status_item['resolved'] = daily_data['resolved']
        status_item['total'] = daily_data['total']
        yield status_item
