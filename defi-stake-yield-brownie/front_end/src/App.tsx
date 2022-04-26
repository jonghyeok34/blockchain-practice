// import React from 'react';
// import logo from './logo.svg';
import { ChainId, Config, DAppProvider, Kovan } from "@usedapp/core";
import "./App.css";
import {Container} from "@mui/material";
import { Header } from "./components/Header";
import { Main } from "./components/Main";
import { getDefaultProvider } from "ethers";

const config: Config = {
  readOnlyChainId: ChainId.Kovan,
  readOnlyUrls: {
    [Kovan.chainId]: getDefaultProvider('kovan')
  },
  notifications:{
    expirationPeriod: 1000, // miliseconds
    checkInterval: 1000
  }
};

function App() {
  return (
    <DAppProvider
    config={config}
    >
      <Header/>
      <Container maxWidth="md">
      
        <Main/>
      </Container>
        
    </DAppProvider>
  );
}

export default App;
