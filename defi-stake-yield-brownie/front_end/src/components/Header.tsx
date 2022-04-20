import { useEthers } from "@usedapp/core";
// import {makeStyles} from "@mui/styles"
import { Button } from "@mui/material";
import { makeStyles } from "@mui/styles";
const useStyles = makeStyles({
  container: {
    padding: 4,
    display: "flex",
    justifyContent: "flex-end",
    gap: 1,
  },
});
export const Header = () => {
  const classes = useStyles();
  const { account, activateBrowserWallet, deactivate } = useEthers();

  const isConnected = account !== undefined;
  return (
    <div className={classes.container}>
      <div>
        {isConnected ? (
          <Button color="primary" variant="contained" onClick={deactivate}>
            Disconnect
          </Button>
        ) : (
          <Button color="primary"  variant="contained" onClick={() => activateBrowserWallet()}>
            Connect
          </Button>
        )}
      </div>
    </div>
  );
};
