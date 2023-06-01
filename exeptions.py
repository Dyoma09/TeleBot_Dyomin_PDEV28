import requests
from utilities import ACCESS_KEY
from utilities import keys

from json_dict import dic_t # импорт словаря для тестирования работоспособности бота, без подключения API

class ApiExeption(Exception):
    pass

class Converter():
    @staticmethod
    def get_price(base, quote, amount):
        
        try:
            convert_from = keys[base.lower()]
        except KeyError:
            raise ApiExeption(f'валюта {base} не найдена!')
        
        try:
            convert_to = keys[quote.lower()]
        except KeyError:
            raise ApiExeption(f'валюта {quote} не найдена!')
        
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ApiExeption(f'не удалось обработать количество {amount}!')
        
        if convert_from == convert_to:
            raise ApiExeption('для конвертации нужно выбрать разные валюты!')
        
        ur_l = f'http://api.exchangeratesapi.io/v1/latest?access_key={ACCESS_KEY}&format=1&_gl=1*l7q2yp*_ga*Nzc5ODE4MjUyLjE2ODUxOTA2MTA.*_ga_HGV43FGGVM*MTY4NTIwMTA4MS4yLjEuMTY4NTIwMjA1Ny42MC4wLjA'
        response = requests.get(ur_l).json()
        currencies = response.get('rates')
        
        #currencies = dic_t['rates'] #словарь json для тестирования бота(количество запросов к api сайта-конвертера ограничено)
       
        converted_price = round(currencies[convert_to] / currencies[convert_from] * float(amount), 3)
        return converted_price
