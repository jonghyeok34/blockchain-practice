from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URI, get_account, get_breed, get_account

dog_meta = {
    "PUG": "https://ipfs.io/ipfs/QmZKUjW9j5tBG336Y4NLxnGuw3J96VqU76C2DHF9KPS4c2?filename=default-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmcThh7p4MA2rQpvjbxApBbyNL7nUScu7ZprEE2iiX9t1j?filename=default-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmW4qPbedTL7DS3AgdzMnrw7YKYZB2miLAywJBNZe97kTz?filename=default-ST_BERNARD.json"
}

def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    numbmer_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {numbmer_of_collectibles} tokenIds")
    
    for token_id in range(numbmer_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI if {token_id}")
            set_tokenURI(token_id, advanced_collectible, dog_meta[breed])
            

def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(f"Awsome! You can view your NFT at {OPENSEA_URI.format(nft_contract.address, token_id)}")
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
    