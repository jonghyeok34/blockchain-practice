from brownie import AdvancedCollectible, network

from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template


def main():
    for a in list(AdvancedCollectible):
        print(a, a.tokenCounter())
    advanced_collectible = AdvancedCollectible[-1]
    # print(list(AdvancedCollectible))
    
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        
