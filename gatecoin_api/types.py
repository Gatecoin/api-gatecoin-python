"""Types for attributes and request/response for the API"""
from typing import List
from datetime import datetime

# pylint: disable=locally-disabled,E1101,R0903


class ResponseError:
    """ResponseError class"""

    def __init__(
            self,
            error_code: str = None,
            field_name: str = None,
            message: str = None):
        self.error_code = error_code
        self.field_name = field_name
        self.message = message


class ResponseStatus:
    """ResponseStatus class"""

    def __init__(
            self,
            error_code: str = None,
            message: str = None,
            stack_trace: str = None,
            errors: List[ResponseError] = None):
        self.error_code = error_code
        self.message = message
        self.stack_trace = stack_trace
        self.errors = errors


class CurrencyPair:
    """CurrencyPair class"""

    def __init__(
            self,
            trading_code: str,
            base_currency: str,
            quote_currency: str,
            display_name: str,
            price_decimal_places: int,
            name: str):
        self.trading_code = trading_code
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.display_name = display_name
        self.price_decimal_places = price_decimal_places
        self.name = name


class Limit:
    """Limit class"""

    def __init__(self, price: float, volume: float):
        self.price = price
        self.volume = volume


class Transaction:
    """Transaction class"""

    def __init__(
            self,
            transaction_id: int,
            transaction_time: datetime,
            price: float,
            quantity: float,
            currency_pair: str,
            way: str,
            ask_order_id: str,
            bid_order_id: str):
        self.transaction_id = transaction_id
        self.transaction_time = transaction_time
        self.price = price
        self.quantity = quantity
        self.currency_pair = currency_pair
        self.way = way
        self.ask_order_id = ask_order_id
        self.bid_order_id = bid_order_id

# API response classes


class GetCurrencyPairsResponse:
    """GetCurrencyPairsResponse class"""

    def __init__(
            self,
            currency_pairs: List[CurrencyPair],
            response_status: ResponseStatus):
        self.currency_pairs = currency_pairs
        self.response_status = response_status


class GetMarketDepthResponse:
    """GetMarketDepthResponse class"""

    def __init__(
            self,
            asks: List[Limit],
            bids: List[Limit],
            response_status: ResponseStatus):
        # self.currency = currency :: Removing for now, not receieved in
        # response
        self.asks = asks
        self.bids = bids
        self.response_status = response_status


class GetOrderBookResponse:
    """GetOrderBookResponse class"""

    def __init__(self, asks: List[Limit], bids: List[Limit]):
        # self.currency = currency :: Removing for now, not receieved in
        # response
        self.asks = asks
        self.bids = bids
        # self.response_status = response_status :: Removing for now, not
        # received in response


class GetRecentTransactionsResponse:
    """GetRecentTransactionsResponse class"""

    def __init__(
            self,
            transactions: List[Transaction],
            response_status: ResponseStatus):
        self.transactions = transactions
        self.response_status = response_status
