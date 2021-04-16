import requests
import json
from config import valuta

class APIException(Exception):
    pass

class ValutaConverter:
    @staticmethod
    def get_price(quote = str, base = str, amount = str):
        if quote == base:
            raise APIException(f'Нельзя перевести одинаковые валюты! {base}')

        try:
            quote_ticker = valuta[quote]
        except KeyError:
            raise APIException(f'В данный момент такой валюты в боте нет - {quote}.')

        try:
            base_ticker = valuta[base]
        except KeyError:
            raise APIException(f'В данный момент такой валюты в боте нет - {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        price = json.loads(r.content)[valuta[base]] * amount

        return price

