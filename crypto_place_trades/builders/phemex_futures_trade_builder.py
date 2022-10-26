import pandas as pd


class PhemexFuturesTradeBuilder:
    LEVERAGE_MIN = 1

    def __init__(self, markets, phemex_client):
        self.markets = markets
        self.phemex_client = phemex_client

    def build(self, trade: pd.Series):
        ticker = "{}/USD:USD".format(
            trade["Asset"].replace("USDPERP", "").replace("100", "100 ").replace("1000", "1000 "))
        market = self.markets[ticker]
        contract_size_raw = market["info"]["contractSize"]
        contract_size = float(contract_size_raw.split()[0])

        return {"ticker": ticker,
                "order_type": "LimitIfTouched",
                "side": "buy" if trade["Direction"] == "long" else "sell",
                "leverage": self.__parse_leverage(trade),
                "amount": trade["Position"] / contract_size,
                "price": trade["Entry price"],
                "params": {"stopPxEp": self.phemex_client.to_ep(trade["Entry price"], market),
                           "triggerType": "ByLastPrice",
                           "takeProfitEp": self.phemex_client.to_ep(trade["Profit target 1"], market),
                           "tpTrigger": "ByLastPrice",
                           "stopLossEp": self.phemex_client.to_ep(trade["Stop loss"], market),
                           "slTrigger": "ByLastPrice"}
                }

    def __parse_leverage(self, trade):
        leverage = round(trade["Leverage"], 2)
        return leverage if leverage > self.LEVERAGE_MIN else self.LEVERAGE_MIN
