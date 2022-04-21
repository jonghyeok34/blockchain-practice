import { useEthers, useTokenBalance } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import { Token } from "../Main";

export interface WalletBalanceProps {
  token: Token;
}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
  const { image, address, name } = token;
  const { account } = useEthers();
  
  const tokenBalance = useTokenBalance(address, account);
  
  const formattedTokenBalance:number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)):0;
  return (
    <div>I'm the wallet balance {formattedTokenBalance}</div>
  );
};
