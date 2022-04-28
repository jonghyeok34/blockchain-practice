import {
  Button,
  CircularProgress,
  Input,
  Alert,
  Snackbar,
} from "@mui/material";
import { useEthers, useNotifications, useTokenBalance } from "@usedapp/core";
import { utils } from "ethers";
import { formatUnits } from "ethers/lib/utils";
import React, { useEffect, useState } from "react";
import { useStakeTokens } from "../../hooks/useStakeTokens";
import { Token } from "../Main";

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
  const [showErc20ApprovalSuccess, setShowErc20ApprovalSuccess] =
    useState(false);
  const [showStakeTokenSuccess, setStakeTokenSuccess] = useState(false);
  const handleCloseSnack = () => {
    setShowErc20ApprovalSuccess(false);
    setStakeTokenSuccess(false);
  }
  useEffect(() => {
    if (
      notifications.filter(
        (notification) =>
          notification.type === "transactionSucceed" &&
          notification.transactionName === "Approve ERC20 transfer"
      ).length > 0
    ) {
      setShowErc20ApprovalSuccess(true);
      setStakeTokenSuccess(false);
      console.log("Approved!");
    }
    if (
      notifications.filter(
        (notification) =>
          notification.type === "transactionSucceed" &&
          notification.transactionName === "Stake tokens"
      ).length > 0
    ) {
      setShowErc20ApprovalSuccess(false);
      setStakeTokenSuccess(true);
    }
  }, [notifications, showErc20ApprovalSuccess, showStakeTokenSuccess]);

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
      <Snackbar open={showErc20ApprovalSuccess} autoHideDuration={5000} onClose={handleCloseSnack}>
        <Alert severity="success">
          ERC-20 token transfer approved! Now approve the 2nd transction
        </Alert>
      </Snackbar>

      <Snackbar open={showStakeTokenSuccess} autoHideDuration={5000} onClose={handleCloseSnack}>
        <Alert severity="success">Tokens Staked!</Alert>
      </Snackbar>
    </>
  );
};
