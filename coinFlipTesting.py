from web3 import Web3
import json
from web3 import Web3, HTTPProvider
# from web3.contract import ConciseContract


ganache_url = 'http://127.0.0.1:7545'

web3  = Web3(Web3.HTTPProvider(ganache_url))

print(web3.isConnected())

###############
# ADDRESSES
###############

# Contract address
file = open('deployContract.txt', 'r')
contractAddr = Web3.toChecksumAddress(file.read())
file.close()


# Owner account
key1="223544fd8827f1006718f557c76665e60a84212b115cd8de8a745b6406e332e0"
ownerAcct = web3.eth.account.privateKeyToAccount(key1)
ownerAcctAddr = ownerAcct.address

# Bet account
key2="b93f0321fd0eee244ac531f98338d643c28adf8d5efdb8cf315c50f0a2d86645"
betAcct = web3.eth.account.privateKeyToAccount(key2)
betAcctAddr = betAcct.address

###################
# SMART CONTRACT
###################

# Access contract json compiled through Truffle
truffleFile = json.load(open('../coinFlipDapp/build/contracts/Flip.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# Contract instance
contractInstance = web3.eth.contract(abi=abi, address=contractAddr)



#######################
# FUND THE CONTRACT
#######################

# # Construct the transaction to fund the contract
# fundAmt = web3.toWei(15,'ether');
#
# nonce = web3.eth.getTransactionCount(ownerAcctAddr)
#
# tx = {
#             'to': contractAddr,
#             'from': ownerAcctAddr,
#             'value': fundAmt,
#             'gas': 2000000,
#             'gasPrice': web3.toWei('40', 'gwei'),
#             'nonce': nonce
#     }
#
# # Fund the contract
# txHash = contractInstance.functions.fundContract().transact(tx)
# print("txHash: {}".format(txHash.hex()))
#
# web3.eth.waitForTransactionReceipt(txHash)

####################
# COIN FLIP BET
####################

# # Construct the transaction to place the bet
# betAmt = web3.toWei(3,'ether');
#
# nonce = web3.eth.getTransactionCount(betAcctAddr)
#
# tx = {
#             'to': contractAddr,
#             'from': betAcctAddr,
#             'value': betAmt,
#             'gas': 2000000,
#             'gasPrice': web3.toWei('40', 'gwei'),
#             'nonce': nonce
#     }
#
# # Fund the contract
# txHash = contractInstance.functions.coinFlip(betAmt).transact(tx)
# print("txHash: {}".format(txHash.hex()))
#
# web3.eth.waitForTransactionReceipt(txHash)

###########################
# WITHDRAW FROM CONTRACT
###########################

# # Construct the transaction to withdraw
# wtdrwAmt = web3.toWei(20,'ether');
#
# nonce = web3.eth.getTransactionCount(ownerAcctAddr)
#
# tx = {
#             'to': contractAddr,
#             'from': ownerAcctAddr,
#             'gas': 2000000,
#             'gasPrice': web3.toWei('40', 'gwei'),
#             'nonce': nonce
#     }

# # Withdraw specific amount from the contract
# txHash = contractInstance.functions.withdraw(wtdrwAmt).transact(tx)
# print("txHash: {}".format(txHash.hex()))
#
# Withdraw all from the contract
# txHash = contractInstance.functions.withdrawAll().transact(tx)
# print("txHash: {}".format(txHash.hex()))
#
#
# web3.eth.waitForTransactionReceipt(txHash)


#print('Withdraw value: {}'.format(contractInstance.functions.withdrawAll().call()))
#print('Withdraw value: {}'.format(contractInstance.functions.withdraw(web3.toWei(3,'ether')).call()))

# print('Bet result: {}'.format(contractInstance.functions.coinFlip(web3.toWei(2,'ether')).call()))

#print("Contract events: {}".format(contractInstance.events.funded.createFilter(fromBlock="0x0").get_all_entries()))
# print("Contract events: {}".format(contractInstance.events.coinFlipped.createFilter(fromBlock="0x0").get_all_entries()))

print('Contract value: {}'.format(contractInstance.functions.getBalance().call()))


# signed_txn = acct.signTransaction(tx)
# txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
