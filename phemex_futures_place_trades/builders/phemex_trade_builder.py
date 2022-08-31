import pandas as pd


class PhemexTradeBuilder:
    PRICE_SCALE = 10000
    LEVERAGE_MIN = 1

    def __init__(self, markets):
        self.markets = markets

    def build(self, trade: pd.Series):
        ticker = "{}/USD:USD".format(trade["Asset"].replace("USDT", ""))
        contract_size_raw = self.markets[ticker]["info"]["contractSize"]
        contract_size = float(contract_size_raw.split()[0])

        return {"ticker": ticker,
                "order_type": "LimitIfTouched",
                "side": "buy" if trade["Direction"] == "long" else "sell",
                "leverage": self.__parse_leverage(trade),
                "amount": trade["Position"] / contract_size,
                "price": trade["Entry price"],
                "params": {"stopPxEp": int(trade["Entry price"] * self.PRICE_SCALE),
                           "triggerType": "ByLastPrice",
                           "takeProfitEp": int(trade["Profit target 1"] * self.PRICE_SCALE),
                           "tpTrigger": "ByLastPrice",
                           "stopLossEp": int(trade["Stop loss"] * self.PRICE_SCALE),
                           "slTrigger": "ByLastPrice"}
                }

    def __parse_leverage(self, trade):
        leverage = round(trade["Leverage"], 2)
        return leverage if leverage > self.LEVERAGE_MIN else self.LEVERAGE_MIN
