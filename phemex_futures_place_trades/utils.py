import logging

import pandas as pd
import yaml


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


def load_trades(direction: str, portfolio: str, trades_excel_path: str) -> pd.DataFrame:
    logging.debug("Loading {} trades from excel for portfolio {}".format(direction, portfolio))
    sheet_name = "TradesLong" if direction == "long" else "TradesShort"
    trades = pd.read_excel(trades_excel_path, sheet_name=sheet_name)
    trades_filtered = trades[trades["On exchange"] == portfolio]
    trades_filtered["Direction"] = direction

    logging.debug("Loaded {} trades for portfolio {}".format(trades_filtered.shape[0], portfolio))
    return trades_filtered
