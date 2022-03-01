from scripts.helpful_scripts import fund_with_link, get_account, OPENSEA_URI, get_contract
from brownie import AdvancedCollectible, config, network

sample_token_uri = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)


def deploy_and_create():
    account = get_account()
    network_config = config["networks"][network.show_active()]
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        network_config["keyhash"],
        network_config["fee"],
        {"from": account},
    )
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created!")
    
def main():
    deploy_and_create()
