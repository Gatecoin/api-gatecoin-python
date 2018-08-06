"""Types for attributes and request/response for the API"""
from datetime import datetime
from typing import List

import pytz
from marshmallow import Schema, fields, post_load, pre_load

from .types import (AccountBalance, CancelAllOpenOrdersResponse,
                    CancelOpenOrderResponse, CreateOrderResponse, CurrencyPair,
                    GetBalanceResponse, GetBalancesResponse,
                    GetCurrencyPairsResponse, GetMarketDepthResponse,
                    GetOpenOrderResponse, GetOpenOrdersResponse,
                    GetOrderBookResponse, GetRecentTransactionsResponse,
                    GetTradeHistoryResponse, Limit, OpenOrder, ResponseError,
                    ResponseStatus, TraderTransaction, Transaction)


class TransactionTimeMixin:
    """Mixin to convert unix timestamp to datetime string for schema"""

    @pre_load(pass_many=True)
    def transform_timestamp(self, data, many):
        """OrderedLimit is the same as Limit but only without keys"""
        if many is True:
            for transaction in data:
                transaction['transactionTime'] = datetime.fromtimestamp(
                    float(transaction['transactionTime']), tz=pytz.utc).isoformat()
            return data
        else:
            data['transactionTime'] = datetime.fromtimestamp(
                float(data['transactionTime']), tz=pytz.utc).isoformat()
            return data

class DateMixin:
    """Mixin to convert unix timestamp to datetime string for schema"""

    @pre_load(pass_many=True)
    def transform_timestamp(self, data, many):
        """OrderedLimit is the same as Limit but only without keys"""
        if many is True:
            for transaction in data:
                transaction['date'] = datetime.fromtimestamp(
                    float(transaction['date']), tz=pytz.utc).isoformat()
            return data
        else:
            data['date'] = datetime.fromtimestamp(
                float(data['date']), tz=pytz.utc).isoformat()
            return data

class ResponseErrorSchema(Schema):
    """ResponseError schema"""
    error_code = fields.Str(load_from='errorCode')
    field_name = fields.Str(load_from='fieldName')
    message = fields.Str()

    @post_load
    def make_object(self, data):
        return ResponseError(**data)


class ResponseStatusSchema(Schema):
    """ResponseStatus schema"""
    error_code = fields.Str(load_from='errorCode')
    message = fields.Str()
    stack_trace = fields.Str(load_from='stackTrace')
    errors = fields.List(fields.Nested(ResponseErrorSchema))

    @post_load
    def make_object(self, data):
        return ResponseStatus(**data)


class ResponseStatusMixin:
    """Mixin to introduce response_status into the schema"""
    response_status = fields.Nested(
        ResponseStatusSchema, load_from='responseStatus')


class CurrencyPairSchema(Schema):
    """CurrencyPair schema"""
    trading_code = fields.Str(load_from='tradingCode')
    base_currency = fields.Str(load_from='baseCurrency')
    quote_currency = fields.Str(load_from='quoteCurrency')
    display_name = fields.Str(load_from='displayName')
    price_decimal_places = fields.Int(
        load_from='priceDecimalPlaces')
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return CurrencyPair(**data)


class LimitSchema(Schema):
    """Limit schema"""
    price = fields.Float()
    volume = fields.Float()

    @post_load
    def make_object(self, data):
        return Limit(**data)


class OrderedLimitSchema(LimitSchema):
    """OrderedLimit schema"""

    @pre_load(pass_many=True)
    def transform_to_dict(self, data, many):
        """OrderedLimit is the same as Limit but only without keys"""
        if many is True:
            proxied = List()
            for limit in data:
                proxied.append({'price': limit[0], 'volume': limit[1]})
            return proxied
        else:
            return {'price': data[0], 'volume': data[1]}


class TransactionSchema(Schema, TransactionTimeMixin):
    """Transaction schema"""
    transaction_id = fields.Integer(load_from='transactionId')
    transaction_time = fields.DateTime(
        load_from='transactionTime')
    price = fields.Float()
    quantity = fields.Float()
    currency_pair = fields.Str(load_from='currencyPair')
    way = fields.Str()
    ask_order_id = fields.Str(load_from='askOrderId')
    bid_order_id = fields.Str(load_from='bidOrderId')

    @post_load
    def make_object(self, data):
        return Transaction(**data)


class AccountBalanceSchema(Schema):
    """AccountBalance schema"""
    currency = fields.Str()
    balance = fields.Float()
    available_balance = fields.Float(load_from='availableBalance')
    pending_incoming = fields.Float(load_from='pendingIncoming')
    pending_outgoing = fields.Float(load_from='pendingOutgoing')
    open_order = fields.Float(load_from='openOrder')
    pledging = fields.Float()
    is_digital = fields.Bool(load_from='isDigital')

    @post_load
    def make_object(self, data):
        return AccountBalance(**data)

class TraderTransactionSchema(Schema, TransactionTimeMixin):
    """TraderTransaction schema"""
    transaction_id = fields.Int(load_from='transactionId')
    transaction_time = fields.DateTime(load_from='transactionTime')
    ask_order_id = fields.Str(load_from='askOrderId')
    bid_order_id = fields.Str(load_from='bidOrderId')
    price = fields.Float()
    quantity = fields.Float()
    currency_pair = fields.Str(load_from='currencyPair')
    way = fields.Str()
    fee_roll = fields.Str(load_from='feeRoll')
    fee_rate = fields.Float(load_from='feeRate')
    fee_amount = fields.Float(load_from='feeAmount')

    @post_load
    def make_object(self, data):
        return TraderTransaction(**data)

class OpenOrderSchema(Schema, DateMixin):
    """OpenOrder schema"""
    code = fields.Str()
    cl_order_id = fields.Str(load_from='clOrderId')
    side = fields.Int()
    price = fields.Float()
    initial_quantity = fields.Float(load_from='initialQuantity')
    remaining_quantity = fields.Float(load_from='remainingQuantity')
    status = fields.Int()
    status_desc = fields.Str(load_from='statusDesc')
    transaction_sequence_number = fields.Int(load_from='transSeqNo')
    type = fields.Int()
    date = fields.DateTime()

    @post_load
    def make_object(self, data):
        return OpenOrder(**data)

# API response schemas


class GetCurrencyPairsResponseSchema(Schema, ResponseStatusMixin):
    """GetCurrencyPairsResponse schema"""
    currency_pairs = fields.List(fields.Nested(
        CurrencyPairSchema), load_from='currencyPairs')

    @post_load
    def make_object(self, data):
        return GetCurrencyPairsResponse(**data)


get_currency_pairs_response_schema = GetCurrencyPairsResponseSchema()


class GetMarketDepthResponseSchema(Schema, ResponseStatusMixin):
    """GetMarketDepthResponse schema"""
    # currency = fields.Str(required=True) :: Removing for now, not receieved
    # in response
    asks = fields.List(fields.Nested(LimitSchema))
    bids = fields.List(fields.Nested(LimitSchema))

    @post_load
    def make_object(self, data):
        return GetMarketDepthResponse(**data)


get_market_depth_response_schema = GetMarketDepthResponseSchema()


class GetOrderBookResponseSchema(Schema):
    """GetOrderBookResponse schema"""
    asks = fields.List(fields.Nested(OrderedLimitSchema))
    bids = fields.List(fields.Nested(OrderedLimitSchema))

    @post_load
    def make_object(self, data):
        return GetOrderBookResponse(**data)


get_order_book_response_schema = GetOrderBookResponseSchema()


class GetRecentTransactionsResponseSchema(Schema, ResponseStatusMixin):
    """GetRecentTransactionsResponse schema"""
    transactions = fields.List(fields.Nested(TransactionSchema))

    @post_load
    def make_object(self, data):
        return GetRecentTransactionsResponse(**data)


get_recent_transactions_response_schema = GetRecentTransactionsResponseSchema()

class GetBalancesResponseSchema(Schema, ResponseStatusMixin):
    """GetBalancesResponse schema"""
    balances = fields.List(fields.Nested(AccountBalanceSchema))

    @post_load
    def make_object(self, data):
        return GetBalancesResponse(**data)


get_balances_response_schema = GetBalancesResponseSchema()

class GetBalanceResponseSchema(Schema, ResponseStatusMixin):
    """GetBalanceResponse schema"""
    balance = fields.Nested(AccountBalanceSchema)

    @post_load
    def make_object(self, data):
        return GetBalanceResponse(**data)


get_balance_response_schema = GetBalanceResponseSchema()

class GetOpenOrdersResponseSchema(Schema, ResponseStatusMixin):
    """GetOpenOrdersResponse schema"""
    orders = fields.List(fields.Nested(OpenOrderSchema))
    
    @post_load
    def make_object(self, data):
        return GetOpenOrdersResponse(**data)

get_open_orders_response_schema = GetOpenOrdersResponseSchema()

class GetOpenOrderResponseSchema(Schema, ResponseStatusMixin):
    """GetOpenOrderResponse schema"""
    order = fields.Nested(OpenOrderSchema)
    
    @post_load
    def make_object(self, data):
        return GetOpenOrderResponse(**data)

get_open_order_response_schema = GetOpenOrderResponseSchema()

class CreateOrderResponseSchema(Schema, ResponseStatusMixin):
    """CreateOrderResponse schema"""
    cl_order_id = fields.Str(load_from='clOrderId')
    order_status = fields.Str(load_from='orderStatus')
    
    @post_load
    def make_object(self, data):
        return CreateOrderResponse(**data)

create_order_response_schema = CreateOrderResponseSchema()

class CancelOpenOrderResponseSchema(Schema, ResponseStatusMixin):
    """CancelOpenOrderResponse schema"""
    
    @post_load
    def make_object(self, data):
        return CancelOpenOrderResponse(**data)

cancel_open_order_response_schema = CancelOpenOrderResponseSchema()

class CancelAllOpenOrdersResponseSchema(Schema, ResponseStatusMixin):
    """CancelAllOpenOrdersResponse schema"""
    
    @post_load
    def make_object(self, data):
        return CancelAllOpenOrdersResponse(**data)

cancel_all_open_orders_response_schema = CancelAllOpenOrdersResponseSchema()

class GetTradeHistoryResponseSchema(Schema, ResponseStatusMixin):
    """GetTradeHistoryResponse schema"""
    trades = fields.List(fields.Nested(TraderTransactionSchema))
    
    @post_load
    def make_object(self, data):
        return GetTradeHistoryResponse(**data)

get_trade_history_response_schema = GetTradeHistoryResponseSchema()
