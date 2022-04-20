// import React from 'react';
// import logo from './logo.svg';
import { ChainId, DAppProvider } from "@usedapp/core";
import "./App.css";
import {Container} from "@mui/material";
import { Header } from "./components/Header";
import { Main } from "./components/Main";

function App() {
  return (
    <DAppProvider
    config={{
      supportedChains: [ChainId.Kovan],
    }}
    >
      <Header/>
      <Container maxWidth="md">
      
        <Main/>
      </Container>
        
    </DAppProvider>
  );
}

export default App;
