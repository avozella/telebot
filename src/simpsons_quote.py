import json
import requests


def simpsons_quote():

    quote = requests.get('https://los-simpsons-quotes.herokuapp.com/v1/quotes')
    items = json.loads(quote.text)

    if quote.status_code == 200:
        for item in items:
            return (item['quote'] + " - " + item['author'])
