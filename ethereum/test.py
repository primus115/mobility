import web3
from web3 import Web3, HTTPProvider
from getpass import getpass  
import json

with open("./build/MobilityAccountABI.json") as f:
    info_json = json.load(f)
abi = info_json

w3 = Web3(HTTPProvider("https://rinkeby.infura.io/v3/23d1d5956dc54a068ab6887ef8e711b3"))
profile = w3.eth.contract(address='0x088F3f5ecd1fAE0B91Ffe84E8f8925a4B297Bf30', abi=abi)
print('Default contract greeting: {}'.format( profile.functions.getIsPaid(2).call() ))

pw = getpass(prompt='Enter the password for decryption: ')

with open('data.json') as keyfile:
    encrypted_key = keyfile.read()
pk = w3.eth.account.decrypt(encrypted_key, pw)
print(pk)

transaction = {
    'value': Web3.toWei(0.01, "ether"),
    'nonce': w3.eth.getTransactionCount('0xB76AC1f39edCa9087dBcaa832B3169cCE0E8Dc65')
}
txn = profile.functions.payRide(5).buildTransaction(transaction)
signed_txn = w3.eth.account.signTransaction(txn, private_key=pk)
w3.eth.sendRawTransaction(signed_txn.rawTransaction)

