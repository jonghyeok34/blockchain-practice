from brownie import AdvancedCollectible, network

from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template

from pathlib import Path
import requests

def main():
    advanced_collectible = AdvancedCollectible[-1]
    # print(list(AdvancedCollectible))
    
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (f"./metadata/{network.show_active()}/{token_id}-{breed}.json")
        print(metadata_file_name)
        
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists")
        else:
            print(f"Creating metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/"+ breed.lower().replace("_","-") +".png"
            image_uri = upload_to_ipfs(image_path)
            

# curl -X POST -F file=@metadata/rinkeby/ "http://127.0.0.1:5001/api/v0/add?quiet=<value>&quieter=<value>&silent=<value>&progress=<value>&trickle=<value>&only-hash=<value>&wrap-with-directory=<value>&chunker=size-262144&pin=true&raw-leaves=<value>&nocopy=<value>&fscache=<value>&cid-version=<value>&hash=sha2-256&inline=<value>&inline-limit=32"

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # upload stuff
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(url=ipfs_url +endpoint, files={"file":image_binary})
        ipfs_hash = response.json()["Hash"]
        # ./img/PUG.png --> PUG.png
        
        filename = filepath.split("/")[-1:][0]   
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}" 
        print(image_uri)
        return image_uri