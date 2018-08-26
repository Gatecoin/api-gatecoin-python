"""API client module for Gatecoin REST API"""

from .constants import HTTPMethod
from .request import Request
from .schemas import (cancel_all_open_orders_response_schema,
                      cancel_open_order_response_schema,
                      create_order_response_schema,
                      get_balance_response_schema,
                      get_balances_response_schema,
                      get_currency_pairs_response_schema,
                      get_market_depth_response_schema,
                      get_open_order_response_schema,
                      get_open_orders_response_schema,
                      get_order_book_response_schema,
                      get_recent_transactions_response_schema,
                      get_trade_history_response_schema)
from .types import (CancelAllOpenOrdersResponse, CancelOpenOrderResponse,
                    CreateOrderResponse, GetBalanceResponse,
                    GetBalancesResponse, GetCurrencyPairsResponse,
                    GetMarketDepthResponse, GetOpenOrderResponse,
                    GetOpenOrdersResponse, GetOrderBookResponse,
                    GetRecentTransactionsResponse, GetTradeHistoryResponse)


class GatecoinAPI:
    """Gatecoin API class"""
    public_key = ''
    private_key = ''

    def __init__(self, private_key: str = None, public_key: str = None):
            self.private_key = private_key
            self.public_key = public_key

    def _handle_response(self, obj, err):
        if err is not None and bool(err) is True:
            return None

        return obj

    def set_credentials(self, private_key: str, public_key: str) -> None:
        """Set public and private key credentials for API"""
        self.private_key = private_key
        self.public_key = public_key

    # The following methods are in the public domain
    # of the API and can be used without setting API
    # credentials first
    def get_currency_pairs(self) -> GetCurrencyPairsResponse:
        """Get currency pairs"""
        response = Request(self.private_key, self.public_key,
                           'v1/Reference/CurrencyPairs').send()
        obj, err = get_currency_pairs_response_schema.load(
            response, partial=True)

        return self._handle_response(obj, err)

    def get_market_depth(self, currency_pair: str) -> GetMarketDepthResponse:
        """Get currency pair market depth"""
        response = Request(self.private_key, self.public_key,
                           'v1/Public/MarketDepth/{0}'.format(currency_pair)).send()
        obj, err = get_market_depth_response_schema.load(
            response, partial=True)

        return self._handle_response(obj, err)

    def get_order_book(self, currency_pair: str) -> GetOrderBookResponse:
        """Get currency pair order book"""
        response = Request(self.private_key, self.public_key,
                           'v1/{0}/OrderBook'.format(currency_pair)).send()
        obj, err = get_order_book_response_schema.load(response, partial=True)

        return self._handle_response(obj, err)

    def get_recent_transactions(self, currency_pair: str) -> GetRecentTransactionsResponse:
        """Get recent transactions for the currency pair"""
        response = Request(self.private_key, self.public_key,
                           'v1/Public/Transactions/{0}'.format(currency_pair)).send()
        obj, err = get_recent_transactions_response_schema.load(
            response, partial=True)

        return self._handle_response(obj, err)

    # The following methods are in the trading
    # domain of the API and must be used only
    # after credentials have been set otherwise
    # the response will always be a failure
    def get_balances(self) -> GetBalancesResponse:
        """Get all balances"""
        response = Request(self.private_key, self.public_key,
                           'v1/Balance/Balances').send()
        obj, err = get_balances_response_schema.load(response, partial=True)

        return self._handle_response(obj, err)

    def get_balance(self, currency_code: str) -> GetBalanceResponse:
        """Get specific currency balance"""
        response = Request(self.private_key, self.public_key,
                           'v1/Balance/Balances').send()
        if 'balances' in response:
            response['balance'] = next(balance for balance in response['balances'] if balance['currency'] == currency_code)

        obj, err = get_balance_response_schema.load(response, partial=True)

        return self._handle_response(obj, err)

    def get_open_orders(self) -> GetOpenOrdersResponse:
        """Get all open orders"""
        response = Request(self.private_key, self.public_key,
                           'v1/Trade/Orders').send()
        obj, err = get_open_orders_response_schema.load(response, partial=True)

        return self._handle_response(obj, err)

    def get_open_order(self, order_id: str) -> GetOpenOrderResponse:
        """Get specific open order"""
        response = Request(self.private_key, self.public_key,
                           'v1/Trade/Orders/{0}'.format(order_id)).send()
        obj, err = get_open_order_response_schema.load(response, partial=True)

        return self._handle_response(obj, err)

    def create_order(
            self,
            currency_pair: str,
            order_way: str,
            price: float,
            amount: float = None,
            spend_amount: float = None,
            external_order_id: str = None,
            validation_code: str = None) -> CreateOrderResponse:
        """Place new order"""
        params = {
            'Code': currency_pair,
            'Way': order_way,
            'Price': price
        }

        if amount is not None:
            params['Amount'] = amount
        if spend_amount is not None:
            params['SpendAmount'] = spend_amount
        if external_order_id is not None:
            params['ExternalOrderId'] = external_order_id
        if validation_code is not None:
            params['ValidationCode'] = validation_code

        response = Request(self.private_key, self.public_key,
                           'v1/Trade/Orders', HTTPMethod.POST, params).send()
        obj, err = create_order_response_schema.load(response, partial=True)

        return self._handle_response(obj, err)

    def cancel_order(self, order_id: str) -> CancelOpenOrderResponse:
        """Cancel an active order"""
        params = {
            'OrderID': order_id
        }

        response = Request(self.private_key, self.public_key,
                           'v1/Trade/Orders/{0}'.format(order_id), HTTPMethod.DELETE, params).send()
        obj, err = cancel_open_order_response_schema.load(
            response, partial=True)

        return self._handle_response(obj, err)

    def cancel_all_orders(self) -> CancelAllOpenOrdersResponse:
        """Cancel all active orders"""
        response = Request(self.private_key, self.public_key,
                           'v1/Trade/Orders', HTTPMethod.DELETE).send()
        obj, err = cancel_all_open_orders_response_schema.load(
            response, partial=True)

        return self._handle_response(obj, err)

    def get_trade_history(self) -> GetTradeHistoryResponse:
        """Get trade history"""
        response = Request(self.private_key, self.public_key,
                           'v1/Trade/TradeHistory').send()
        obj, err = get_trade_history_response_schema.load(
            response, partial=True)

        return self._handle_response(obj, err)
