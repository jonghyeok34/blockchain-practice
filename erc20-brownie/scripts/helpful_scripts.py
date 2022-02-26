from brownie import (
    network, 
    config, 
    accounts
)
from web3 import Web3
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 2000 * (10 ** DECIMALS)

GAS_LIMIT_WEI_DICT = {
    "rinkeby": 20000000,
    "ganache-local": 6721975
}
GAS_LIMIT_WEI = 29000000 if network.show_active() =="rinkeby" else 6721975

def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

