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
            trading_code: str = None,
            base_currency: str = None,
            quote_currency: str = None,
            display_name: str = None,
            price_decimal_places: int = None,
            name: str = None):
        self.trading_code = trading_code
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.display_name = display_name
        self.price_decimal_places = price_decimal_places
        self.name = name


class Limit:
    """Limit class"""

    def __init__(self, price: float = None, volume: float = None):
        self.price = price
        self.volume = volume


class Transaction:
    """Transaction class"""

    def __init__(
            self,
            transaction_id: int = None,
            transaction_time: datetime = None,
            price: float = None,
            quantity: float = None,
            currency_pair: str = None,
            way: str = None,
            ask_order_id: str = None,
            bid_order_id: str = None):
        self.transaction_id = transaction_id
        self.transaction_time = transaction_time
        self.price = price
        self.quantity = quantity
        self.currency_pair = currency_pair
        self.way = way
        self.ask_order_id = ask_order_id
        self.bid_order_id = bid_order_id

class AccountBalance:
    """AccountBalance class"""

    def __init__(self, currency: str = None, balance: float = None, available_balance: float = None, pending_incoming: float = None, pending_outgoing: float = None, open_order: float = None, pledging: float = None, is_digital: bool = None):
        self.currency = currency
        self.balance = balance
        self.available_balance = available_balance
        self.pending_incoming = pending_incoming
        self.pending_outgoing = pending_outgoing
        self.open_order = open_order
        self.pledging = pledging
        self.is_digital = is_digital

class TraderTransaction:
    """TraderTransaction class"""
    def __init__(self, transaction_id: int = None, transaction_time: datetime = None, ask_order_id: str = None, bid_order_id: str = None, price: float = None, quantity: float = None, currency_pair: str = None, way: str = None, fee_roll: str = None, fee_rate: float = None, fee_amount: float = None):
        self.transaction_id = transaction_id
        self.transaction_time = transaction_time
        self.ask_order_id = ask_order_id
        self.bid_order_id = bid_order_id
        self.price = price
        self.quantity = quantity
        self.currency_pair = currency_pair
        self.way = way
        self.fee_roll = fee_roll
        self.fee_rate = fee_rate
        self.fee_amount = fee_amount

class OpenOrder:
    """OpenOrder class"""

    def __init__(self, code: str = None, cl_order_id: str = None, side: int = None, price: float = None, initial_quantity: float = None, remaining_quantity: float = None, status: int = None, status_desc: str = None, transaction_sequence_number: int = None, type: int = None, date: datetime = None, trades: List[TraderTransaction] = None):
        self.code = code
        self.cl_order_id = cl_order_id
        self.side = side
        self.price = price
        self.initial_quantity = initial_quantity
        self.remaining_quantity = remaining_quantity
        self.status = status
        self.status_desc = status_desc
        self.transaction_sequence_number = transaction_sequence_number
        self.type = type
        self.date = date
        self.trades = trades


# API response classes


class GetCurrencyPairsResponse:
    """GetCurrencyPairsResponse class"""

    def __init__(
            self,
            currency_pairs: List[CurrencyPair] = None,
            response_status: ResponseStatus = None):
        self.currency_pairs = currency_pairs
        self.response_status = response_status


class GetMarketDepthResponse:
    """GetMarketDepthResponse class"""

    def __init__(
            self,
            asks: List[Limit] = None,
            bids: List[Limit] = None,
            response_status: ResponseStatus = None):
        # self.currency = currency :: Removing for now, not receieved in
        # response
        self.asks = asks
        self.bids = bids
        self.response_status = response_status


class GetOrderBookResponse:
    """GetOrderBookResponse class"""

    def __init__(self, asks: List[Limit] = None, bids: List[Limit] = None):
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
            transactions: List[Transaction] = None,
            response_status: ResponseStatus = None):
        self.transactions = transactions
        self.response_status = response_status


class GetBalancesResponse:
    """GetBalancesResponse class"""

    def __init__(
            self,
            balances: List[AccountBalance] = None,
            response_status: ResponseStatus = None):
        self.balances = balances
        self.response_status = response_status

class GetBalanceResponse:
    """GetBalanceResponse class"""

    def __init__(
            self,
            balance: AccountBalance = None,
            response_status: ResponseStatus = None):
        self.balance = balance
        self.response_status = response_status


class GetOpenOrdersResponse:
    """GetOpenOrdersResponse class"""

    def __init__(self, orders: List[OpenOrder], response_status: ResponseStatus):
        self.orders = orders
        self.response_status = response_status

class GetOpenOrderResponse:
    """GetOpenOrderResponse class"""

    def __init__(self, order: OpenOrder, response_status: ResponseStatus):
        self.order = order
        self.response_status = response_status

class CreateOrderResponse:
    """CreateOrderResponse class"""

    def __init__(self, cl_order_id: str = None, order_status: str = None, response_status: ResponseStatus = None):
        self.cl_order_id = cl_order_id
        self.order_status = order_status
        self.response_status = response_status

class CancelOpenOrderResponse:
    """CancelOpenOrderResponse class"""
    
    def __init__(self, response_status: ResponseStatus = None):
        self.response_status = response_status

class CancelAllOpenOrdersResponse:
    """CancelAllOpenOrdersResponse class"""
    
    def __init__(self, response_status: ResponseStatus = None):
        self.response_status = response_status

class GetTradeHistoryResponse:
    """GetTradeHistoryResponse class"""
    
    def __init__(self, trades: List[TraderTransaction] = None, response_status: ResponseStatus = None):
        self.trades = trades
        self.response_status = response_status