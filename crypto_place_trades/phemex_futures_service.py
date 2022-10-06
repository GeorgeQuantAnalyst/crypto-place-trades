import logging

import pandas as pd

from crypto_place_trades.builders.phemex_futures_trade_builder import PhemexFuturesTradeBuilder
from crypto_place_trades.utils import load_trades
from crypto_place_trades.validators.phemex_futures_trade_validator import PhemexFuturesTradeValidator


class PhemexFuturesService:
    SEPARATOR = "---------------------------------------------"

    def __init__(self, phemex_client_account1, phemex_client_account2):
        self.phemex_client_account1 = phemex_client_account1
        self.phemex_client_account2 = phemex_client_account2
        self.markets = phemex_client_account1.load_markets()
        self.phemex_trade_builder = PhemexFuturesTradeBuilder(self.markets, phemex_client_account1)
        self.trade_validator = PhemexFuturesTradeValidator(self.markets)

    def place_trades_on_exchange(self, account: str):
        logging.info("Start place trades on Phemex futures exchange - account {}".format(account))
        trades_long = load_trades("long", account, "data/phemex_futures_trades.xlsx")
        trades_short = load_trades("short", account, "data/phemex_futures_trades.xlsx")
        self.__place_trades_on_exchange(trades_long, account)
        self.__place_trades_on_exchange(trades_short, account)
        logging.info("Finished place trades on Phemex futures exchange - account {}".format(account))
        pass

    def __place_trades_on_exchange(self, trades: pd.DataFrame, account: str):
        phemex_client = self.phemex_client_account1 if account == "A1" else self.phemex_client_account2
        logging.info(self.SEPARATOR)
        logging.info("Start place trades on exchange")
        logging.info(self.SEPARATOR + "\n")

        for index, trade in trades.iterrows():
            validate_errors = self.trade_validator.validate(trade)
            if len(validate_errors) > 0:
                self.__log_trade_error(trade, "Skip trade because contains validations error")
                self.__log_trade_error(trade, "Trade inputs: {}", trade)
                self.__log_trade_error(trade, "Validation errors: {}", validate_errors)
                continue

            phemex_trade = self.phemex_trade_builder.build(trade)

            self.__log_trade_info(trade, "Start place trade on Phemex exchange")
            self.__log_estimate_pnl_info(trade)
            leverage_response = phemex_client.set_leverage(phemex_trade["leverage"], phemex_trade["ticker"])
            if self.__is_successful_set_leverage(leverage_response):
                self.__log_trade_info(trade, "Successfully set leverage {}", phemex_trade["leverage"])
            else:
                self.__log_trade_error(trade, "Error in set leverage {}", phemex_trade["leverage"])
                self.__log_trade_error(trade, "Leverage response:", leverage_response)
                self.__log_trade_error(trade, "Skip trade because not correct set leverage.")
                continue

            create_order_response = phemex_client.create_order(
                phemex_trade["ticker"],
                phemex_trade["order_type"],
                phemex_trade["side"],
                phemex_trade["amount"],
                phemex_trade["price"],
                phemex_trade["params"])

            if self.__is_successful_place_trade(create_order_response):
                self.__log_trade_info(trade, "Successfully place on Phemex exchange. 🌟 🐟 🐻")
            else:
                self.__log_trade_error(trade, "Error in place trade on Phemex exchange")
                self.__log_trade_error(trade, "Create order response: {}", create_order_response)
                continue

            self.__log_trade_info(trade, "Finished place trade on Phemex exchange\n")

        logging.info(self.SEPARATOR)
        logging.info("Finished place trades on Phemex exchange")
        logging.info(self.SEPARATOR)

    @staticmethod
    def __is_successful_set_leverage(leverage_response):
        logging.debug("Leverage response: {}".format(leverage_response))
        return leverage_response["code"] == "0" and leverage_response["data"] == "OK"

    @staticmethod
    def __is_successful_place_trade(create_order_response):
        logging.debug("Create order response: {}".format(create_order_response))
        return create_order_response["info"]["bizError"] == "0"

    @staticmethod
    def __log_trade_info(trade, message, params=[]):
        info_message = "Trade {}-{}: " + message
        logging.info(info_message.format(
            trade["Asset"],
            trade["Direction"],
            params
        ))

    @staticmethod
    def __log_trade_error(trade, message, params=[]):
        error_message = "Trade {}-{}: " + message
        logging.info(error_message.format(
            trade["Asset"],
            trade["Direction"],
            params
        ))

    def __log_estimate_pnl_info(self, trade):
        if trade["Direction"] == "long":
            estimated_profit = (trade["Profit target 1"] - trade["Entry price"]) * trade["Position"]
            estimated_loss = (trade["Stop loss"] - trade["Entry price"]) * trade["Position"]

            pt_m = "If Last Price goes up to {}, it will trigger market order Take Profit estimated profit: {} USD." \
                .format(trade["Profit target 1"], round(estimated_profit, 2))
            self.__log_trade_info(trade, pt_m)

            sl_m = "If Last Price goes down to {}, it will trigger market order Stop Loss estimated loss: {} USD." \
                .format(trade["Stop loss"], round(estimated_loss, 2))
            self.__log_trade_info(trade, sl_m)
        else:
            estimated_profit = (trade["Entry price"] - trade["Profit target 1"]) * trade["Position"]
            estimated_loss = (trade["Entry price"] - trade["Stop loss"]) * trade["Position"]

            pt_m = "If Last Price goes down to {}, it will trigger market order Take Profit estimated profit: {} USD." \
                .format(trade["Profit target 1"], round(estimated_profit, 2))
            self.__log_trade_info(trade, pt_m)

            sl_m = "If Last Price goes up to {}, it will trigger market order Stop Loss estimated loss: {} USD." \
                .format(trade["Stop loss"], round(estimated_loss, 2))
            self.__log_trade_info(trade, sl_m)
