// Where the tokenURI can be one of 3 different dogs
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 internal keyHash;
    uint256 internal fee;
    uint256 public randomNumber;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyHash, uint256 _fee) public 
    VRFConsumerBase(_vrfCoordinator, _linkToken) 
    ERC721("Dogie", "DOG") {

        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }


    function createCollectible() public returns (bytes32){
        bytes32 requestId = getRandomness();
        mintNewOne();
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
        
    }
    
    function getRandomness() public returns (bytes32) {
        require(
            LINK.balanceOf(address(this)) >= fee,
            "Inadequate Link to fund this transaction"
        );
        return requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        randomNumber = randomness;
    }

    function mintNewOne() internal{
        Breed breed = Breed(randomNumber %3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        // address owner = requestIdToSender[requestId];
        _safeMint(msg.sender, newTokenId);
        // _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter +1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // pub, shiba inu, st bernard
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner no approved");
        _setTokenURI(tokenId, _tokenURI);
    }

}