# libraries
- aave 관련: https://github.com/PatrickAlphaC/aave_brownie_py
- chainlink : https://github.com/smartcontractkit/chainlink - AggregatorV3Interface(v0.6)

# 추가
- kovan address:  https://aave.github.io/aave-addresses/kovan.json
# 단계
1. swap ETH to WETH
   1. https://kovan.etherscan.io/token/0xd0a1e359811322d97991e03f863a0c30c2cf029c
2. Deposit some ETH (WETH) into Aave
3. Borrow some asset with the ETH collateral
   1. Sell that borrwed asset. (Short selling)
4. Repay everything back

- paraswap, uniswap ...


Testing:

- Integration test: Kovan
- Unit tests : mainnet-fork