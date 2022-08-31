import logging

import pandas as pd

from phemex_futures_place_trades.builders.phemex_trade_builder import PhemexTradeBuilder
from phemex_futures_place_trades.validators.trade_validator import TradeValidator


class PhemexService:
    def __int__(self, phemex_client):
        self.phemex_client = phemex_client

    def place_trades_on_exchange(self, trades: pd.DateFrame):
        logging.info("Start place trades on exchange")
        for trade in trades:
            validate_errors = TradeValidator.validate(trade)
            if len(validate_errors) > 0:
                logging.error(
                    "Trade {}-{}: Skip trade because contains validations error".format(
                        trade["Asset"],
                        trade["Direction"]))
                logging.error("Trade {}-{}: Trade inputs: {}".format(
                    trade["Asset"],
                    trade["Direction"],
                    trade))
                logging.error("Trade {}-{}: Validations error: {}".format(
                    trade["Asset"],
                    trade["Direction"],
                    validate_errors))
                continue
            phemex_trade = PhemexTradeBuilder.build(trade)

            logging.info("Trade {}-{}: start place trade on exchange".format(
                phemex_trade["ticker"],
                phemex_trade["direction"]
            ))
            leverage_response = self.phemex_client.set_leverage(phemex_trade["leverage"], phemex_trade["ticker"])
            if self.__is_successful_set_leverage(leverage_response):
                logging.info("Trade {}-{}: Successfully set leverage {}".format(
                    phemex_trade["ticker"],
                    phemex_trade["direction"],
                    phemex_trade["leverage"]))
            else:
                logging.error(
                    "Trade {}-{}: Error in set leverage {}".format(
                        phemex_trade["ticker"],
                        phemex_trade["direction"],
                        phemex_trade["leverage"]))
                logging.error("Trade {}-{}: leverage response: {}".format(
                    phemex_trade["ticker"],
                    phemex_trade["direction"],
                    leverage_response))
                logging.error(
                    "Trade {}-{}: skip trade because not correct set leverage.".format(
                        phemex_trade["ticker"],
                        phemex_trade["direction"]
                    ))
                continue

            create_order_response = self.phemex_client.create_order(
                phemex_trade["ticker"],
                phemex_trade["order_type"],
                phemex_trade["side"],
                phemex_trade["amount"],
                phemex_trade["Entry price"],
                phemex_trade["params"])

            if self.__is_successful_place_trade(create_order_response):
                logging.info("Trade {}-{}: successfully place on Phemex exchange.".format(
                    phemex_trade["ticker"],
                    phemex_trade["direction"]
                ))
            else:
                logging.error("Trade {}-{}: error in place trade on exchange".format(
                    phemex_trade["ticker"],
                    phemex_trade["direction"]
                ))
                logging.error("Trade {}-{}: Create order response: {}".format(
                    phemex_trade["ticker"],
                    phemex_trade["direction"],
                    create_order_response
                ))
                continue

            logging.info("Trade {}-{}: finished place to exchange".format(
                phemex_trade["ticker"],
                phemex_trade["direction"]
            ))

        logging.info("Start place trades on exchange")

    @staticmethod
    def __is_successful_set_leverage(leverage_response):
        # TODO: implement me
        return False

    @staticmethod
    def __is_successful_place_trade(create_order_response):
        # TODO: implement me
        return False
