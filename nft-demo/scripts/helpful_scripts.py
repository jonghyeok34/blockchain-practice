from brownie import (
    Contract,
    accounts,
    network,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
)
from web3 import Web3

GAS_LIMIT_WEI_DICT = {
    "rinkeby": 29900000,
    "ganache-local": 6721975
}
GAS_LIMIT_WEI = GAS_LIMIT_WEI_DICT[network.show_active()] if GAS_LIMIT_WEI_DICT.get(network.show_active()) else 6721975

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache", "mainnet-fork"]
OPENSEA_URI = "https://testnets.opensea.io/assets/{}/{}"

DECIMALS = 8
INITIAL_VALUE = 2000 * 10 ** 8


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}
BREED_MAPPING = {0:"PUG", 1:"SHIBA_INU", 2:"ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]    


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    """This functino will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract

        Args:
            contact_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recentl deployed version of this contract.

    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # MockV3Aggregator.length
            deploy_mocks()
        print(list(contract_type))
        contract = contract_type[-1]
        # MOockV3Aggegator[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print("Deploying Mock LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock VRF Coordinator...")
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})

def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.25, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    print(f"link_token:{link_token}")
    print(f"funding_tx:{contract_address}, {amount}")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account, "gas_limit": GAS_LIMIT_WEI/100, "gas_price": 22000000000})
    funding_tx.wait(1)
    
    print(f"Funded {contract_address}")
    
    