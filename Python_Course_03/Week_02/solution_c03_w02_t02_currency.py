import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def get_valute(valutes, cur_from):
    try:
        res = [valute for valute in valutes if valute.charcode.string == cur_from][0]
    except IndexError:
        res = None
    return res


def convert(amount, cur_from, cur_to, date, requests=requests):
    api = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req=' + str(date)
    response = requests.get(api)
    soup = BeautifulSoup(response.text, 'lxml')
    valutes = soup.find_all('valute')

    valute_from = get_valute(valutes, cur_from)
    valute_to = get_valute(valutes, cur_to)

    rate_from = nomn_from = rate_to = nomn_to = 1

    if valute_from:
        rate_from = float(valute_from.value.string.replace(',', '.'))
        nomn_from = float(valute_from.nominal.string.replace(',', '.'))
    if valute_to:
        rate_to = float(valute_to.value.string.replace(',', '.'))
        nomn_to = float(valute_to.nominal.string.replace(',', '.'))

    rate = rate_from * nomn_to / (rate_to * nomn_from)
    result = Decimal(str(round(float(amount) * rate, 4)))

    return result

'''
res = convert(100, 'USD', 'AZN', '02/03/2020')
print(res)
res = convert('100', 'USD', 'AZN', '02/03/2020')
print(res)
'''
