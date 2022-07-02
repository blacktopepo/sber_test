import json
import re

import requests
from bs4 import BeautifulSoup


class Client:
    url = 'https://www.fedstat.ru/indicator/59146'
    keys = {
        'years': '3',
        'regions': '3301',
    }

    def __init__(self):
        src = self.get_data()
        self.soup = BeautifulSoup(src, 'lxml')
        self.filters_data = self.get_filters_data()
        self.years = self.get_values('years')
        self.regions = self.get_values('regions')

    # def get_data(self) -> str:
    #     response = requests.get(self.url)
    #     return response.text

    @staticmethod
    def get_data():
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()

    def get_values(self, key) -> tuple[str]:
        """Получаем список значений для POST запроса"""
        values: dict = self.filters_data[self.keys[key]]['values']
        return tuple(values.keys())

    @staticmethod
    def get_slice_filters(script) -> str:
        """Из js кода вытаскиваем строку, в которой описывается json объект"""
        start_phrase = 'filters:'
        start = script.find(start_phrase)
        end = script.find('left_columns:')

        return script[start + len(start_phrase):end - 2]

    def get_python_object(self, script):
        raw_str = self.get_slice_filters(script)

        quote_keys_regex = r'([\{\s,])(\w+)(:)'
        raw_str = re.sub(quote_keys_regex, r'\1"\2"\3', raw_str)
        raw_str = re.sub(r"'\S*'", '""', raw_str)

        return json.loads(raw_str)

    def get_filters_data(self) -> dict:
        """Получаем объект с данными для параметров POST запроса"""
        script = self.soup.find(
            'script', text=re.compile('filters')
        ).text.replace(' ', '')
        return self.get_python_object(script)
