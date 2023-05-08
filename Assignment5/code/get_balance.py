#!/bin/env python3

from web3 import Web3
import SEEDWeb3

def print_balance(_web3, address):
    if address != None:
       caddr = Web3.to_checksum_address(address)
       print("{}: {}".format(caddr, _web3.eth.get_balance(caddr)))
    else:
       print("Address is None!")

web3 = SEEDWeb3.connect_to_geth_poa('http://10.151.0.71:8545')

# Get the balance of the accounts on the geth node 
print("----------------------------------------------------------")
print("*** This client program connects to 10.151.0.71:8545")
print("*** The following are the accounts on this Ethereum node")
for acct in web3.eth.accounts:
    print_balance(web3, acct)
print("----------------------------------------------------------")


# Get the balances of the victim's and attacker's contract accounts.
# Please use their correct addresses.
try:
  victim_addr = '0x4Ca22C34ff84123aEBac6facd7DEf9ccc9BED38e'
  print("  Victim: ", end='')
  print_balance(web3, victim_addr)

  attack_addr = '0x508b995749FeDc4248e16fCa1121D55DF992B537'
  print("Attacker: ", end='')
  print_balance(web3, attack_addr)
except:
  print()
  print("Exception captured: Please put the actual address in the code")
