import pandas as pd


class TradeValidator:
    LEVERAGE_MIN = 1
    LEVERAGE_MAX = 20

    @staticmethod
    def validate(trade: pd.Series):
        errors = []

        # TODO: implement me
        if True:
            errors.append("some error")

        return errors
