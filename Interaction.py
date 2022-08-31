from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests

def postTransaction(sender, receiver, amount, type):
    transaction = sender.createTransaction(receiver.publicKeyString(), amount, type)
    url = 'http://localhost:5001/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)

if __name__ == '__main__':
    
    sam = Wallet()
    tom = Wallet()
    tom.fromKey('keys/stakerPrivateKey.pem')
    exchange = Wallet()
    
    postTransaction(exchange, tom, 1000, 'EXCHANGE')
    postTransaction(exchange, sam, 1000, 'EXCHANGE')
    postTransaction(exchange, sam, 100, 'EXCHANGE')
    
    
    postTransaction(tom, tom, 250, 'STAKE')
    postTransaction(tom, sam, 10, 'TRANSFER')
    postTransaction(tom, sam, 10, 'TRANSFER')
    postTransaction(tom, sam, 10, 'TRANSFER')
    