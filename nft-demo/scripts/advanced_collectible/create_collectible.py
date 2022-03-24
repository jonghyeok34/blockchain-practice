from brownie import AdvancedCollectible, accounts
from web3 import Web3
from scripts.helpful_scripts import fund_with_link, get_account
def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    print(advanced_collectible)
    print("fund_with_link")
    fund_with_link(advanced_collectible.address, amount= Web3.toWei(0.1, "ether"))
    print("advanced_collectible.createCollectible")
    creation_transaction = advanced_collectible.createCollectible({"from": account, "gas_limit": 2900000, "gas_price": 2200000000, "allow_revert": True})
    creation_transaction.wait(1)
    print("Collectible created")
    