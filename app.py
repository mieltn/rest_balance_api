from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from urls import URLS

# initialize app, reference database and configure database connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Client(db.Model):
    '''
    Table model to store clients.
    Clients have ids and balances.
    '''

    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)

    def serialize(self):
        return {
            'client_id': self.id,
            'balance': self.balance,
        }


class Transaction(db.Model):
    '''
    Table model to store transactions.
    Transactions have ids, amounts and seller/buyer keys refrencing to clients table.
    Clients reference is useful to update balances, when transfer is requested.
    '''

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    seller_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

    seller = db.relationship('Client', foreign_keys=[seller_id])
    buyer = db.relationship('Client', foreign_keys=[buyer_id])


    def serialize(self):
        return {
            'transaction_id': self.id,
            'amount': self.amount,
            'seller_id': self.seller_id,
            'buyer_id': self.buyer_id
        }


@app.get('/api/client/balance/<int:client_id>')
def getBalance(client_id):
    '''
    Gets balance of a particular user.
    Client id should be sent in get request url.
    Returns status and client instance.
    '''
    client = Client.query.get_or_404(client_id)
    if request.args:
        currency = request.args['currency']
        r = requests.get(URLS['currency']).json()
        return jsonify(
            status=200,
            output={
                'client_id': client.id,
                'balance': client.balance * r['data'][currency],
                'currency': currency
            }
        )

    return jsonify(
        status=200,
        output=client.serialize()
    )


@app.post('/api/client/add')
def addClient():
    '''
    Adds new client to database.
    Uses post method and json argument to provide balance for new client.
    Returns status and added client instance.
    '''

    if request.is_json:
        new_client = Client(
            balance = request.json['balance']
        )
            
        db.session.add(new_client)
        db.session.commit()
        return jsonify(
            status=201,
            added=new_client.serialize()
        )

    return jsonify(
        status=400,
        message='Pass valid json argument to the request header'
    )


@app.patch('/api/client/update/<int:client_id>')
def updateBalance(client_id):
    '''
    Increases or decreases balance of a given client.
    Client id should be sent in request url.
    Action and amount should be provided with json argument in patch request.
    '''

    if request.is_json:
        client = Client.query.get_or_404(client_id)
        amount = request.json['amount']

        # if action = credit, we need to increase balance
        # else before action we check if amount is less or equal to available balance
        if request.json['action'] == 'credit':
            client.balance += amount
        else:
            if amount > client.balance:
                return jsonify(
                    status=501, 
                    message=f'Failed to update balance. Not enough money on buyer\'s account',
                    client=client.serialize()
                )
            client.balance -= amount
        db.session.commit()

        return jsonify(
            status=200,
            updated=client.serialize()
        )

    return jsonify(
        status=400,
        message='Pass valid json argument to the request header'
    )


@app.post('/api/transaction')
def addTransaction():
    '''
    Performs new transaction.
    Checks if buyer and seller are presented in clients table.
    If not, adds them with 0 balances.
    Checks balance of buyer, to be sure that the requsted amount could be provided.
    Updates balances of buyer and seller.
    Adds transaction to database.
    '''

    if request.is_json:

        seller_id = request.json['seller_id']
        buyer_id = request.json['buyer_id']
        # variable to check if provided clients exist
        seller_exists = Client.query.get(seller_id)
        buyer_exists = Client.query.get(buyer_id)

        # if any of clients absent, call client add method
        params = {'balance': 0}
        if not seller_exists:
            seller_resp = requests.post(URLS['add'], json=params).json()
            seller_id = seller_resp['added']['client_id']

        if not buyer_exists:
            buyer_resp = requests.post(URLS['add'], json=params).json()
            buyer_id = buyer_resp['added']['client_id']

        # update balances and add transaction
        amount = request.json['amount']

        # first, try to call update on buyer to make sure there are enougth money
        params_buyer = {'amount': amount, 'action': 'writeoff'}
        update_buyer_resp = requests.patch(URLS['update'] + str(buyer_id), json=params_buyer).json()
        # if request was executed successfully, update seller balance
        # then add new transaction to database
        if update_buyer_resp['status'] == 200:
            params_seller = {'amount': amount, 'action': 'credit'}
            update_seller_resp = requests.patch(URLS['update'] + str(seller_id), json=params_seller).json()
            
            new_transaction = Transaction(
                amount = amount,
                seller_id = seller_id,
                buyer_id = buyer_id,
            )

            db.session.add(new_transaction)
            db.session.commit()

            return jsonify(
                status=201,
                added=new_transaction.serialize()
            )

        return update_buyer_resp
        