from web3 import Web3
import json
from web3 import Web3, HTTPProvider


def DeployContract():

    # Connect to Ganache
    ganache_url = 'http://127.0.0.1:7545'
    web3  = Web3(Web3.HTTPProvider(ganache_url))

    #print(web3.isConnected())

    pkey1 = '223544fd8827f1006718f557c76665e60a84212b115cd8de8a745b6406e332e0'
    # pkey1 = "<Private Key here with 0x prefix>"
    acct = web3.eth.account.privateKeyToAccount(pkey1)

    ########################
    # DEPLOY THE CONTRACT
    ########################

    # Access smart contract compiled with Truffle
    truffleFile = json.load(open('../coinFlipDapp/build/contracts/Flip.json'))
    abi = truffleFile['abi']
    bytecode = truffleFile['bytecode']
    contract= web3.eth.contract(bytecode=bytecode, abi=abi)

    # Create nonce
    nonce = web3.eth.getTransactionCount(acct.address)

    # Build transaction to deploy contract
    construct_txn = contract.constructor().buildTransaction({
        'from': acct.address,
        'nonce': nonce,
        'gas': 1728712,
        'gasPrice': web3.toWei('21', 'gwei')})

    # Sign transaction
    signed_tx = acct.signTransaction(construct_txn)

    # Transaction hash
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    #print(tx_hash.hex())

    # Contract address
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    #print("Contract Deployed At:", tx_receipt['contractAddress'])

    # with open('deployContract.txt', 'w') as outfile:
    #     outfile.write(tx_receipt['contractAddress'])

    # Erase existing content
    file = open('deployContract.txt','w')
    file.close()

    # Store contract address
    file = open('deployContract.txt','w')
    file.write(tx_receipt['contractAddress'])
    file.close()


def FundContract():

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

    # Owner account
    key1="223544fd8827f1006718f557c76665e60a84212b115cd8de8a745b6406e332e0"
    ownerAcct = web3.eth.account.privateKeyToAccount(key1)
    ownerAcctAddr = ownerAcct.address


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

    # Construct the transaction to fund the contract
    fundAmt = web3.toWei(15,'ether');

    nonce = web3.eth.getTransactionCount(ownerAcctAddr)

    tx = {
                'to': contractAddr,
                'from': ownerAcctAddr,
                'value': fundAmt,
                'gas': 2000000,
                'gasPrice': web3.toWei('40', 'gwei'),
                'nonce': nonce
        }

    # Fund the contract
    txHash = contractInstance.functions.fundContract().transact(tx)
    #print("txHash: {}".format(txHash.hex()))

    web3.eth.waitForTransactionReceipt(txHash)

    print('Contract value: {}'.format(contractInstance.functions.getBalance().call()))
