import logging.config
import sys

import ccxt

from crypto_place_trades import __version__
from crypto_place_trades.okx_spot_service import OkxSpotService
from crypto_place_trades.phemex_futures_service import PhemexFuturesService
from crypto_place_trades.utils import load_config

# Constants
__logo__ = """
---------------------------------------------------------------------
crypto-place-trades {}
---------------------------------------------------------------------
""".format(__version__.__version__)
CONFIG_FILE_PATH = "config.yaml"
LOGGER_CONFIG_FILE_PATH = "logger.conf"
TRADES_EXCEL_PATH = "data/trades_{}.xlsx"

# Init
logging.config.fileConfig(fname=LOGGER_CONFIG_FILE_PATH, disable_existing_loggers=False)
logging.info(__logo__)
config = load_config(CONFIG_FILE_PATH)

phemex_client_account1 = ccxt.phemex({
    "apiKey": config["phemexApiAccount1"]["apiKey"],
    "secret": config["phemexApiAccount1"]["secretKey"],
    'options': {'defaultType': 'swap'}
})
phemex_client_account2 = ccxt.phemex({
    "apiKey": config["phemexApiAccount2"]["apiKey"],
    "secret": config["phemexApiAccount2"]["secretKey"],
    'options': {'defaultType': 'swap'}
})

okx_client = ccxt.okx()

if __name__ == "__main__":
    try:
        phemex_futures_service = PhemexFuturesService(phemex_client_account1, phemex_client_account2)
        okx_spot_service = OkxSpotService(okx_client)

        exchange = sys.argv[1]
        if exchange == "PhemexFuturesAccount1":
            phemex_futures_service.place_trades_on_exchange(account=1)

        if exchange == "PhemexFuturesAccount2":
            phemex_futures_service.place_trades_on_exchange(account=2)

        if exchange == "OkxSpot":
            okx_spot_service.place_trades_on_exchange()


    except:
        logging.exception("Error in application:")
        sys.exit(1)
