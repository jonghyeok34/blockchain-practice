import { Box, Tab } from "@mui/material";
import { TabContext, TabList, TabPanel} from "@mui/lab";
import { Token } from "../Main";
import {WalletBalance} from "./WalletBalance";
import React, { useState } from "react";

interface YourWalletProps {
  supportedTokens: Array<Token>;
}

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0);
    const handleChange = (event:React.ChangeEvent<{}>, newValue: string) => {
      setSelectedTokenIndex(parseInt(newValue));
    };
    return (
    <Box>
      <h1>Your Wallet</h1>
      <Box>
        <TabContext value={selectedTokenIndex.toString()}>
            <TabList onChange={handleChange} aria-label="stake form tabs">
                {supportedTokens.map((token, index) => {
                    return (
                        <Tab label={token.name}
                        value={index.toString()}
                        key={index}
                        />
                    )
                })}
            </TabList>
            {supportedTokens.map((token, index) => {
              return (
                <TabPanel value={index.toString()} key={index}>
                  <div>
                    {token.address}

                    <WalletBalance token={supportedTokens[selectedTokenIndex]}></WalletBalance>
                    2. a big stake button

                  </div>
                </TabPanel>
              )
            })}
        </TabContext>
      </Box>
    </Box>
  );
};
