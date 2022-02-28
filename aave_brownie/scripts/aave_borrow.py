from brownie import config, network, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import  get_weth
from web3 import Web3

amount = Web3.toWei(0.1, "ether")
INTEREST_RATE_MODE = {
    "STABLE": 1,
    "VARIABLE": 2
}
def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    
    lending_pool = get_lending_pool()
    # Approve sending out ERC20 tokens
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing..")
    tx = lending_pool.deposit(erc20_address, amount, account.address, 0, {"from": account})
    tx.wait(1)
    print("Deposited!")
    # borrow
    # 0.1 ETH deposited --> 0.08 can be borrowed
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    print("start borrowing")
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"])
    # borrowable_eth -> borrowable_Dai * 95%
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address, 
        Web3.toWei(amount_dai_to_borrow, "ether"),
        INTEREST_RATE_MODE["STABLE"],
        0,
        account.address,
        {"from":account}
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI")
    get_borrowable_data(lending_pool, account)
    # repay_all(amount, lending_pool, account)
    print("Deposited, borrowed, and repayed with Aave, brownie and chainlink")
    
def repay_all(amount, lending_pool, account):
    dai_token_address = config["networks"][network.show_active()]["dai_token"]
    approve_erc20(
        Web3.toWei(amount, "ether"), 
        lending_pool, 
        dai_token_address,
        account
    )
    repay_tx = lending_pool.repay(
        dai_token_address,
        amount,
        INTEREST_RATE_MODE["STABLE"],
        account,
        {"from": account}
    )
    repay_tx.wait(1)
    print("Repayed")
    

def get_asset_price(price_feed_address: str):
    # ABI
    # Address
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    # (
    #     round_id,
    #     answer,
    #     started_at,
    #     updated_at,
    #     answered_in_round
    # )
    dai_eth_price_info = dai_eth_price_feed.latestRoundData()
    converted_latest_price = Web3.fromWei(dai_eth_price_info[1], "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(converted_latest_price)

def get_borrowable_data(lending_pool, account):
    (
       total_collateral_eth,
       total_debt_eth,
       available_borrows_eth,
       current_liquidation_threshold,
       ltv,
       health_factor
    ) = lending_pool.getUserAccountData(account)
    available_borrows_eth = Web3.fromWei(available_borrows_eth, "ether")
    total_collateral_eth= Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth= Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH depositied")
    print(f"You have {total_debt_eth} worth of ETH borrowed")
    print(f"You can borrow {available_borrows_eth} worth of ETH")
    
    return (float(available_borrows_eth), float(total_debt_eth))
    
def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    
    return tx
    
def get_lending_pool():
    # ABI
    # Address
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool