from brownie import interface, config, network

from scripts.helpful_scripts import get_account

ETHEREUM_UNIT = 10 ** 18


def main():
    get_weth()
    
def get_weth():
    '''
    mints WETH by depositing ETH.
    '''
    # ABI
    # Address
    account = get_account()
    print(f"account:{account}")
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from":account, "value": 0.1 * ETHEREUM_UNIT})
    tx.wait(1)
    print(f"Received 0.1 WETH")
    return tx