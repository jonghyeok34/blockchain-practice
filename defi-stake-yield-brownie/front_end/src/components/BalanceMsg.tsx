import { makeStyles } from "@mui/styles";

const useStyles = makeStyles({
    container: {
        display: "inline-grid",
        gridTemplateColumns: "auto auto auto",
        gap: 1,
        alignItems: "center",
    },
    tokenImg:{width: "32px"},
    amount: {
        fontWeight: 700
    }
});

interface BalanceMsgProps {
    label: string
    amount: number
    tokenImgSrc: string
}

export const BalanceMsg = ({label, amount, tokenImgSrc}: BalanceMsgProps) =>{
    const classes = useStyles();
    return (
        <div className={classes.container}>

            <div>{label}</div>
            <div className={classes.amount}>{amount}</div>
            <img className={classes.tokenImg} src={tokenImgSrc} alt="token logo"></img>
        </div>
    )
}