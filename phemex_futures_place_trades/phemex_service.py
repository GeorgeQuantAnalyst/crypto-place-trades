import logging

import pandas as pd

from phemex_futures_place_trades.builders.phemex_trade_builder import PhemexTradeBuilder
from phemex_futures_place_trades.validators.trade_validator import TradeValidator


class PhemexService:
    def __int__(self, phemex_client):
        self.phemex_client = phemex_client
        self.markets = phemex_client.load_markets()
        self.phemex_trade_builder = PhemexTradeBuilder(self.markets)

    def place_trades_on_exchange(self, trades: pd.DateFrame):
        logging.info("Start place trades on exchange")
        for trade in trades:
            validate_errors = TradeValidator.validate(trade)
            if len(validate_errors) > 0:
                self.__log_trade_error(trade, "Skip trade because contains validations error")
                self.__log_trade_error(trade, "Trade inputs: {}", trade)
                self.__log_trade_error(trade, "Validation errors: {}", validate_errors)
                continue

            phemex_trade = self.phemex_trade_builder.build(trade)

            self.__log_trade_info(trade, "start place trade on Phemex exchange")
            leverage_response = self.phemex_client.set_leverage(phemex_trade["leverage"], phemex_trade["ticker"])
            if self.__is_successful_set_leverage(leverage_response):
                self.__log_trade_info(trade, "Successfully set leverage {}", phemex_trade["leverage"])
            else:
                self.__log_trade_error(trade, "Error in set leverage {}", phemex_trade["leverage"])
                self.__log_trade_error(trade, "Leverage response:", leverage_response)
                self.__log_trade_error(trade, "Skip trade because not correct set leverage.")
                continue

            create_order_response = self.phemex_client.create_order(
                phemex_trade["ticker"],
                phemex_trade["order_type"],
                phemex_trade["side"],
                phemex_trade["amount"],
                phemex_trade["Entry price"],
                phemex_trade["params"])

            if self.__is_successful_place_trade(create_order_response):
                self.__log_trade_info(trade, "Successfully place on Phemex exchange.")
            else:
                self.__log_trade_error(trade, "Error in place trade on Phemex exchange")
                self.__log_trade_error(trade, "Create order response: {}", create_order_response)
                continue

            self.__log_trade_info("Finished place trade on Phemex exchange")

        logging.info("Finished place trades on Phemex exchange")

    @staticmethod
    def __is_successful_set_leverage(leverage_response):
        # TODO: implement me
        return False

    @staticmethod
    def __is_successful_place_trade(create_order_response):
        # TODO: implement me
        return False

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
