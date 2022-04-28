/**eslint-disable spaced-comment */
/// <reference types="react" />
import { useEthers } from "@usedapp/core";
import helperConfig from "../helper-config";
import networkMapping from "../chain-info/deployments/map.json";
import { constants } from "ethers";
import brownieConfig from "../brownie-config.json";
import dapp from "../dapp.png";
import eth from "../eth.png";
import dai from "../dai.png";
import { YourWallet } from "./yourWallet/YourWallet";
import { makeStyles } from "@mui/styles";

export type Token = {
  image: string;
  address: string;
  name: string;
};
const useStyles = makeStyles({
  title: {
    color: "white",
    textAlign: "center",
    padding: 4,
  },
});

export const Main = () => {
  const classes = useStyles();
  // show token values from the wallet

  // get the address of different tokens
  // get the balance of the users wallet

  // send the brownie-config to our `src` folder
  // send the build folder
  const { chainId, error } = useEthers();
  const networkName: string = chainId ? helperConfig[chainId] : "dev";
  const dappTokenAddress: string = chainId
    ? networkMapping[String(chainId)]["DappToken"][0]
    : constants.AddressZero;
  const wethTokenAddress: string = chainId
    ? brownieConfig["networks"][networkName]["weth_token"]
    : constants.AddressZero;
  const fauTokenAddress: string = chainId
    ? brownieConfig["networks"][networkName]["fau_token"]
    : constants.AddressZero;

  const supportedTokens: Array<Token> = [
    { image: dapp, address: dappTokenAddress, name: "DAPP" },
    { image: eth, address: wethTokenAddress, name: "WETH" },
    { image: dai, address: fauTokenAddress, name: "FAU" },
  ];

  return (
    <>
    <h2 className={classes.title}>Dapp Token App</h2>
      <YourWallet supportedTokens={supportedTokens}></YourWallet>
    </>
  );
};
