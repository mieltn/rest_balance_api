import requests

def populate(balances):
    '''
    Populate database with clients for testing
    '''

    url = 'http://127.0.0.1:5000/api/client/add'
    for balance in balances:
        params = {'balance': balance}
        r = requests.post(url, json=params)
    return 'ok'


def get_balance(client_id):
    '''
    Test function for getting balance of a given client.
    '''

    url = 'http://127.0.0.1:5000/api/client/balance/'
    r = requests.get(url + str(client_id)).json()
    return r


def update_balance(client_id, amount, action):
    '''
    Test function for updating balance for a given amount.
    Depending on the action received, balance could be increased or decreased.
    '''

    url = 'http://127.0.0.1:5000/api/client/update/'
    params = {'amount': amount, 'action': action}
    r = requests.patch(url + str(client_id), json=params).json()
    return r


def transfer(seller_id, buyer_id, amount):
    '''
    Test function for performing new transaction.
    '''

    url = 'http://127.0.0.1:5000/api/transaction'
    params = {'amount': amount, 'seller_id': seller_id, 'buyer_id': buyer_id}
    r = requests.post(url, json=params).json()
    return r


if __name__ == '__main__':

    # populate db with 5 clients and given balances
    balances = [1, 55, 500, 200, 12.34]
    print(populate(balances))

    # get balance of the third client
    # correct answer: 500
    print(get_balance(3))

    # update balance of the third client
    # first tests credit action for increasing balance
    # second tests writeoff action for decreasing balance
    # after both actions performed the correct balance: 499
    print(update_balance(3, 100, 'credit'))
    print(update_balance(3, 101, 'writeoff'))

    # add new transaction
    # transfer from 4th client to 1st in amount of 20
    # get the balances of clients
    # correct anser: 1 - 21, 4 - 180
    print(transfer(1, 4, 20))
    print(get_balance(1))
    print(get_balance(4))

    