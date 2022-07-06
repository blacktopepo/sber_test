import json
import re

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class Parser:
    """
    Клиент для получения данных со страницы
    https://www.fedstat.ru/indicator/59146
    """
    base_url = 'https://www.fedstat.ru/'
    REGION_PREFIX = '3301'
    prefixes = {
        'years': '3',
        'regions': '3301',
    }

    def __init__(self):
        src = self.get_data_to_parse()
        self.soup = BeautifulSoup(src, 'lxml')
        self.filters_data = self.get_filters_data()

    def get_data_to_parse(self) -> str:
        """Получаем html текст с сайта"""
        url = urljoin(self.base_url, 'indicator/59146')
        response = requests.get(url)
        return response.text

    def get_values(self, key) -> tuple[str, ...]:
        """Получаем список значений для POST запроса"""
        values: dict = self.filters_data[self.prefixes[key]]['values']
        return tuple(values.keys())

    def get_years(self) -> tuple[str, ...]:
        """Возвращает список годов, которые есть в отчёте."""
        return self.get_values('years')

    @staticmethod
    def get_slice_filters(script: str) -> str:
        """Из js кода вытаскиваем строку, в которой описывается json объект"""
        start_phrase = 'filters:'
        start = script.find(start_phrase)
        end = script.find('left_columns:')

        return script[start + len(start_phrase):end - 2]

    def get_python_object(self, script: str):
        """Преобразуем строку кода js в объект python"""
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

    def get_filter_values(self) -> list[str]:
        """Возвращает значения id регионов и года с префиксом для FormData."""
        result = []
        for key, value in self.prefixes.items():
            values = [f'{value}_{el}' for el in self.get_values(key)]
            result.extend(values)
        return result

    def get_result_data(self) -> list[dict]:
        """
        Получаем из API средний индекс качества городской среды по
        регионам РФ за отчётные года.
        """
        url = urljoin(self.base_url, 'indicator/dataGrid.do?id=59146')
        payload = {
            'lineObjectIds': ['0', '3301', '30611'],
            'columnObjectIds': ['3', '33560'],
            'selectedFilterIds': self.get_filter_values()
        }
        response = requests.post(url=url, data=payload)
        return response.json()['results']
