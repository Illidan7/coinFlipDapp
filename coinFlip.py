from web3 import Web3
import json
from web3 import Web3, HTTPProvider

def coinFlipBet(x):

    # Connect to Ganache
    ganache_url = 'http://127.0.0.1:7545'
    web3  = Web3(Web3.HTTPProvider(ganache_url))

    ###############
    # ADDRESSES
    ###############

    # Contract address
    file = open('deployContract.txt', 'r')
    contractAddr = Web3.toChecksumAddress(file.read())
    file.close()

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

    # Contract value
    init = contractInstance.functions.getBalance().call()[0]


    ####################
    # COIN FLIP BET
    ####################

    # Construct the transaction to place the bet
    betAmt = web3.toWei(x,'ether');

    nonce = web3.eth.getTransactionCount(betAcctAddr)

    tx = {
                'to': contractAddr,
                'from': betAcctAddr,
                'value': betAmt,
                'gas': 2000000,
                'gasPrice': web3.toWei('40', 'gwei'),
                'nonce': nonce
        }

    # Fund the contract
    txHash = contractInstance.functions.coinFlip(betAmt).transact(tx)
    #print("txHash: {}".format(txHash.hex()))

    web3.eth.waitForTransactionReceipt(txHash)

    final = contractInstance.functions.getBalance().call()[0]

    if final > init:
        return 0
    else:
        return 1
