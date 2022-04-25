import { Button, Input } from "@mui/material";
import { useEthers, useTokenBalance } from "@usedapp/core";
import { formatUnits } from "ethers/lib/utils";
import React, { useState } from "react";
import { Token } from "../Main";
import {useStakeTokens} from "../../hooks/useStakeTokens";
import { utils } from "ethers";

export interface StakeFormProps {
    token: Token
}
export const StakeForm = ({token}: StakeFormProps) => {
    const {address :tokenAddress ,name} = token;
    const {account} = useEthers();
    const tokenBalance = useTokenBalance(tokenAddress, account);
    const formattedTokenBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)):0;

    const [amount, setAmount] = useState<number | string | Array<number |string>>(0);
    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newAmount = event.target.value === ""? "": Number(event.target.value);
        setAmount(newAmount);
       
    };
    const {approve, approveErc20State} = useStakeTokens(tokenAddress);
    const handleStakeSubmit = () =>
    {
        const amountAsWei = utils.parseEther(amount.toString()).toString();
        return approve(amountAsWei);
    };
    return (

        <>
            <Input
            onChange={handleInputChange}
            />
            <Button color="primary" size="large" onClick={handleStakeSubmit}>
                Stake!
            </Button>
        </>
    
    )
};