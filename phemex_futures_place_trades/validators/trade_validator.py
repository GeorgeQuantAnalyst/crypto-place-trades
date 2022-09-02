import math

import pandas as pd


class TradeValidator:
    LEVERAGE_MAX = 20

    def __init__(self, markets):
        self.markets = markets

    def validate(self, trade: pd.Series):
        missing_attribute_errors = self.__validate_exist_attribute(trade, "Asset") + \
                                   self.__validate_exist_attribute(trade, "Entry price") + \
                                   self.__validate_exist_attribute(trade, "Stop loss") + \
                                   self.__validate_exist_attribute(trade, "Profit target 1") + \
                                   self.__validate_exist_attribute(trade, "Position") + \
                                   self.__validate_exist_attribute(trade, "Leverage") + \
                                   self.__validate_exist_attribute(trade, "Direction")

        if len(missing_attribute_errors) > 0:
            return missing_attribute_errors

        format_errors = self.__validate_exist_ticker_on_exchange(trade["Asset"], self.markets) + \
                        self.__validate_float_number(trade, "Entry price") + \
                        self.__validate_float_number(trade, "Stop loss") + \
                        self.__validate_float_number(trade, "Profit target 1") + \
                        self.__validate_float_number(trade, "Position") + \
                        self.__validate_float_number(trade, "Leverage") + \
                        self.__validate_allowed_values(trade, "Direction", ["long", "short"])

        if len(format_errors) > 0:
            return format_errors

        logic_errors = self.__validate_greater_than_value(trade, "Entry price", 0) + \
                       self.__validate_greater_than_value(trade, "Stop loss", 0) + \
                       self.__validate_greater_than_value(trade, "Profit target 1", 0) + \
                       self.__validate_greater_than_value(trade, "Position", 0) + \
                       self.__validate_greater_than_value(trade, "Leverage", 0) + \
                       self.__validate_smaller_than_value(trade, "Leverage", self.LEVERAGE_MAX + 0.01)

        if trade["Direction"] == "long":
            logic_errors = logic_errors + \
                           self.__validate_greater_than(trade, "Entry price", "Profit target 1") + \
                           self.__validate_smaller_than(trade, "Stop loss", "Entry price")
        else:
            logic_errors = logic_errors + \
                           self.__validate_smaller_than(trade, "Profit target 1", "Entry price") + \
                           self.__validate_greater_than(trade, "Stop loss", "Entry price")

        return logic_errors

    @staticmethod
    def __validate_exist_attribute(trade, attribute):
        validation_errors = []

        if attribute not in trade:
            validation_errors.append("Missing attribute [{}] in trade".format(attribute))

        return validation_errors

    @staticmethod
    def __validate_exist_ticker_on_exchange(asset, markets):
        validation_errors = []
        ticker = "{}/USD:USD".format(asset.replace("USDT", ""))
        if ticker not in markets:
            validation_errors.append("Not valid Asset {} for trading ticker: {}".format(asset, ticker))

        return validation_errors

    @staticmethod
    def __validate_float_number(trade, attribute):
        validation_errors = []
        try:
            float(trade[attribute])
        except ValueError:
            validation_errors.append("Attribute [{}] is not float number: {}".format(attribute, trade[attribute]))

        if math.isnan(trade[attribute]):
            validation_errors.append("Attribute [{}] is not float number: {}".format(attribute, trade[attribute]))

        return validation_errors

    @staticmethod
    def __validate_greater_than(trade, attribute_smaller, attribute_bigger):
        validation_errors = []
        attribute_smaller_value = float(trade[attribute_smaller])
        attribute_bigger_value = float(trade[attribute_bigger])

        if attribute_bigger_value < attribute_smaller_value:
            validation_errors.append("Attribute {} - {} must be greater than attribute {} - {}".format(
                attribute_bigger, attribute_bigger_value,
                attribute_smaller, attribute_smaller_value))

        return validation_errors

    @staticmethod
    def __validate_smaller_than(trade, attribute_smaller, attribute_bigger):
        validation_errors = []
        attribute_smaller_value = float(trade[attribute_smaller])
        attribute_bigger_value = float(trade[attribute_bigger])

        if attribute_smaller_value > attribute_bigger_value:
            validation_errors.append("Attribute {} - {} must be smaller than attribute {} - {}".format(
                attribute_smaller, attribute_smaller_value,
                attribute_bigger, attribute_bigger_value))

        return validation_errors

    @staticmethod
    def __validate_greater_than_value(trade, attribute, value):
        validation_errors = []

        if float(trade[attribute]) < value:
            validation_errors.append("Attribute {} - {} must be greater than {}".format(
                attribute, float(trade[attribute]), value))

        return validation_errors

    @staticmethod
    def __validate_smaller_than_value(trade, attribute, value):
        validation_errors = []

        if float(trade[attribute]) > value:
            validation_errors.append("Attribute {} - {} must be smaller than {}".format(
                attribute, float(trade[attribute]), value))

        return validation_errors

    @staticmethod
    def __validate_allowed_values(trade, attribute, allowed_values):
        validation_errors = []

        if trade[attribute] not in allowed_values:
            validation_errors.append("Attribute [{}] value: {} must be in [{}]".format(
                attribute,
                trade[attribute],
                allowed_values
            ))

        return validation_errors
