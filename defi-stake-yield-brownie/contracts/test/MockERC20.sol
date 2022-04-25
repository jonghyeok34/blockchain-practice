pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MockERC20 is ERC20{ 
    constructor() public ERC20("MockERC20", "MERC20"){
        _mint(msg.sender, 1000000*10*18); 
    }

}