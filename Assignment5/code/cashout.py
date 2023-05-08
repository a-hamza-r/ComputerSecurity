#!/bin/env python3
  
from web3 import Web3
import SEEDWeb3
import os

web3 = SEEDWeb3.connect_to_geth_poa('http://10.151.0.72:8545')

sender_account = web3.eth.accounts[1]
web3.geth.personal.unlock_account(sender_account, "admin")

abi_file      = "../contract/ReentrancyAttacker.abi"
attacker_addr = '0x543151dE5355F3540B4eE437B01E878eA72ff065'

# Cash out the money from the attacker contract
contract_abi   = SEEDWeb3.getFileContent(abi_file)
recipient_acct = Web3.to_checksum_address(web3.eth.accounts[0])
contract = web3.eth.contract(address=attacker_addr, abi=contract_abi)
tx_hash  = contract.functions.cashOut(recipient_acct).transact({ 
                    'from':  sender_account
                })
print("Transaction sent, waiting for block ...")
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("Transaction Receipt: {}".format(tx_receipt))

