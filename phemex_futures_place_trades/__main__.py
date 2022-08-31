import logging
import sys

import ccxt

from phemex_futures_place_trades import __version__
from phemex_futures_place_trades.phemex_service import PhemexService
from phemex_futures_place_trades.utils import parse_portfolio_from_input_parameters, load_config, load_trades

# Constants
__logo__ = """
---------------------------------------------------------------------
phemex-futures-place-trades {}
---------------------------------------------------------------------
""".format(__version__.__version__)
CONFIG_FILE_PATH = "config.yaml"
LOGGER_CONFIG_FILE_PATH = "logger.conf"
TRADES_EXCEL_PATH = "data/trades_{}.xlsx"

# Init
logging.config.fileConfig(fname=LOGGER_CONFIG_FILE_PATH, disable_existing_loggers=False)
logging.info(__logo__)
config = load_config(CONFIG_FILE_PATH)

phemex_client_p1 = ccxt.phemex({
    "apiKey": config["phemexApiPortfolio1"]["apiKey"],
    "secret": config["phemexApiPortfolio1"]["secretKey"],
    'options': {'defaultType': 'swap'}
})
phemex_client_p2 = ccxt.phemex({
    "apiKey": config["phemexApiPortfolio2"]["apiKey"],
    "secret": config["phemexApiPortfolio2"]["secretKey"],
    'options': {'defaultType': 'swap'}
})

if __name__ == "__main__":
    try:
        portfolio = parse_portfolio_from_input_parameters()
        phemex_client = phemex_client_p1 if portfolio == "P1" else phemex_client_p2
        phemex_service = PhemexService(phemex_client)

        logging.info("Start place trades on Phemex exchange - portfolio {}".format(portfolio))
        phemex_service.place_trades_on_exchange(load_trades("long", portfolio))
        phemex_service.place_trades_on_exchange(load_trades("short", portfolio))
        logging.info("Finished place trades on exchange - portfolio {}".format(portfolio))
    except:
        logging.exception("Error in application:")
        sys.exit(1)
