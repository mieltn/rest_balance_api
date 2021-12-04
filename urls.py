API_KEY = 'e1ec72b0-54ea-11ec-91fb-13a5b979b7ff'

URLS = {
    'get': 'http://127.0.0.1:5000/api/client/balance/',
    'add': 'http://127.0.0.1:5000/api/client/add',
    'update': 'http://127.0.0.1:5000/api/client/update/',
    'transfer': 'http://127.0.0.1:5000/api/transaction',
    'currency': 'https://freecurrencyapi.net/api/v2/latest?apikey={}&base_currency=RUB'.format(API_KEY)
}