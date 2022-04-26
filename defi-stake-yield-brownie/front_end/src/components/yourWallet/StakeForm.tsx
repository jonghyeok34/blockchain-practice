import { Button, Input, CircularProgress } from "@mui/material";
import { useEthers, useTokenBalance, useNotifications } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import React, { useEffect, useState } from "react";
import { Token } from "../Main";
import { useStakeTokens } from "../../hooks/useStakeTokens";
import { utils } from "ethers";

export interface StakeFormProps {
  token: Token;
}

export const StakeForm = ({ token }: StakeFormProps) => {
  const { address: tokenAddress, name } = token;
  const { account } = useEthers();
  const tokenBalance = useTokenBalance(tokenAddress, account);
  const formattedTokenBalance: number = tokenBalance
    ? parseFloat(formatUnits(tokenBalance, 18))
    : 0;
  const { notifications } = useNotifications();
  const [amount, setAmount] = useState<
    number | string | Array<number | string>
  >(0);
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newAmount =
      event.target.value === "" ? "" : Number(event.target.value);
    setAmount(newAmount);
  };

  const { approveAndStake, state: approveAndStakeErc20State } =
    useStakeTokens(tokenAddress);
  const handleStakeSubmit = () => {
    const amountAsWei = utils.parseEther(amount.toString());
    return approveAndStake(amountAsWei.toString());
  };

  const isMining = approveAndStakeErc20State.status === "Mining";

  useEffect(() => {
    if (
      notifications.filter(
        (notification) =>
          notification.type === "transactionSucceed" &&
          notification.transactionName === "Approve ERC20 transfer"
      ).length > 0
    ) {
      console.log("Approved!");
    }
    if (
      notifications.filter(
        (notification) =>
          notification.type === "transactionSucceed" &&
          notification.transactionName === "Stake tokens"
      ).length > 0
    ) {
      console.log("Token Staked!");
    }
  }, [notifications]);

  return (
    <>
      <Input onChange={handleInputChange} />
      <Button
        color="primary"
        size="large"
        onClick={handleStakeSubmit}
        disabled={isMining}
      >
        {isMining ? <CircularProgress size={26}></CircularProgress> : "Stake!"}
      </Button>
    </>
  );
};
