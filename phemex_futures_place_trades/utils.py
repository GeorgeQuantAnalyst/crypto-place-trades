import logging
import sys

import pandas as pd
import yaml

TRADES_EXCEL_PATH = "data/trades.xlsx"


def load_config(file_path):
    try:
        with open(file_path, 'r') as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        logging.exception("Problem with loading configuration from file, the application will be terminated.")
        exit(1)
    except yaml.YAMLError:
        logging.exception("Problem with parsing configuration, the application will be terminated.")
        exit(1)


def load_trades(direction: str, portfolio: str) -> pd.DataFrame:
    logging.debug("Loading {} trades from excel for portfolio {}".format(direction, portfolio))
    sheet_name = "TradesLong" if direction == "long" else "TradesShort"
    trades = pd.read_excel(TRADES_EXCEL_PATH, sheet_name=sheet_name)
    trades_filtered = trades[trades["On exchange"] == portfolio]
    trades_filtered["Direction"] = direction
    logging.debug("Loaded {} trades for portfolio {}".format(trades_filtered.shape[0], portfolio))
    return trades_filtered


def parse_portfolio_from_input_parameters():
    if len(sys.argv) < 2 or not (sys.argv[1] == "P1" or sys.argv[1] == "P2"):
        logging.debug("Input parameters: {}".format(sys.argv))
        error_message = """
                Missing or bad argument portfolio, please run app with param:
                python -m phemex_futures_place_trades [P1/P2]
                """
        raise Exception(error_message)

    return sys.argv[1]
