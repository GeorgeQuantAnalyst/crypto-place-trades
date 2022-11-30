import logging.config
import sys

import ccxt

from crypto_place_trades.constants import LOGGER_CONFIG_FILE_PATH, __logo__, CONFIG_FILE_PATH
from crypto_place_trades.okx_spot_service import OkxSpotService
from crypto_place_trades.phemex_futures_service import PhemexFuturesService
from crypto_place_trades.utils import load_config

if __name__ == "__main__":
    logging.config.fileConfig(fname=LOGGER_CONFIG_FILE_PATH, disable_existing_loggers=False)
    logging.info(__logo__)
    config = load_config(CONFIG_FILE_PATH)

    phemex_client_account1 = ccxt.phemex({
        "apiKey": config["exchangeApi"]["phemexApiAccount1"]["apiKey"],
        "secret": config["exchangeApi"]["phemexApiAccount1"]["secretKey"],
        'options': {'defaultType': 'swap'}
    })
    phemex_client_account2 = ccxt.phemex({
        "apiKey": config["exchangeApi"]["phemexApiAccount2"]["apiKey"],
        "secret": config["exchangeApi"]["phemexApiAccount2"]["secretKey"],
        'options': {'defaultType': 'swap'}
    })

    okx_client = ccxt.okx()

    try:
        phemex_futures_service = PhemexFuturesService(phemex_client_account1, phemex_client_account2)
        okx_spot_service = OkxSpotService(okx_client)

        exchange = sys.argv[1]

        match exchange:
            case "PhemexFuturesAccount1":
                phemex_futures_service.place_trades_on_exchange(account="A1")
            case "PhemexFuturesAccount2":
                phemex_futures_service.place_trades_on_exchange(account="A2")
            case "OkxSpot":
                okx_spot_service.place_trades_on_exchange()
            case _:
                raise Exception("Not supported exchange - {}".format(exchange))

    except:
        logging.exception("Error in application:")
        sys.exit(1)
