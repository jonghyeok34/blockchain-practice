// import React from 'react';
// import logo from './logo.svg';
import { ChainId, DAppProvider } from "@usedapp/core";
import "./App.css";
import {Container} from "@mui/material";
import { Header } from "./components/Header";

function App() {
  return (
    <DAppProvider
    config={{
      supportedChains: [ChainId.Kovan, ChainId.Rinkeby],
    }}
    >
      <Header/>
      <Container maxWidth="md">
        <div>Hi!</div>
      </Container>
        
    </DAppProvider>
  );
}

export default App;
