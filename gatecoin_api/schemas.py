"""Types for attributes and request/response for the API"""
import pytz
from datetime import datetime
from typing import List
from marshmallow import Schema, fields, post_load, pre_load
from .types import ResponseError, ResponseStatus, CurrencyPair, GetCurrencyPairsResponse, Limit, Transaction, GetMarketDepthResponse, GetOrderBookResponse, GetRecentTransactionsResponse


def datetime_to_timestamp(value: datetime):
    return value.timestamp()


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
    trading_code = fields.Str(load_from='tradingCode', required=True)
    base_currency = fields.Str(load_from='baseCurrency', required=True)
    quote_currency = fields.Str(load_from='quoteCurrency', required=True)
    display_name = fields.Str(load_from='displayName', required=True)
    price_decimal_places = fields.Int(
        load_from='priceDecimalPlaces', required=True)
    name = fields.Str(required=True)

    @post_load
    def make_object(self, data):
        return CurrencyPair(**data)


class LimitSchema(Schema):
    """Limit schema"""
    price = fields.Float(required=True)
    volume = fields.Float(required=True)

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


class TransactionSchema(Schema):
    """Transaction schema"""
    transaction_id = fields.Integer(load_from='transactionId', required=True)
    transaction_time = fields.DateTime(
        load_from='transactionTime', required=True)
    price = fields.Float(required=True)
    quantity = fields.Float(required=True)
    currency_pair = fields.Str(load_from='currencyPair', required=True)
    way = fields.Str(required=True)
    ask_order_id = fields.Str(load_from='askOrderId', required=True)
    bid_order_id = fields.Str(load_from='bidOrderId', required=True)

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

    @post_load
    def make_object(self, data):
        return Transaction(**data)

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
