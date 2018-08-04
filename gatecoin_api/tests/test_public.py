"""Test suite for Gatecoin REST API public methods"""
import pytest
from datetime import datetime
from gatecoin_api import GatecoinAPI
from gatecoin_api.types import CurrencyPair, Limit, Transaction


def _test_currency_pair(pair: CurrencyPair):
    """Test parsed currency pair structure"""
    assert (pair.trading_code is not None), 'Trading code did not deserialize properly'
    assert (pair.base_currency is not None), 'Base currency did not deserialize properly'
    assert (
        pair.quote_currency is not None), 'Quote currency did not deserialize properly'
    assert (pair.display_name is not None), 'Display name did not deserialize properly'
    assert (pair.name is not None), 'Name did not deserialize properly'
    assert (pair.price_decimal_places is not None), 'Price decimal places did not deserialize properly'


def _test_limit(limit: Limit):
    """Test parsed limit structure"""
    assert (limit.price is not None), 'Price did not deserialize properly'
    assert (limit.volume is not None), 'Volume did not deserialize properly'


def _test_transaction(transaction: Transaction):
    """Test parsed transaction structure"""
    assert (transaction.transaction_id is not None), 'Transaction ID did not deserialize properly'
    assert (transaction.transaction_time is not None), 'Transaction time did not deserialize properly'
    assert (transaction.price is not None), 'Price did not deserialize properly'
    assert (transaction.quantity is not None), 'Quantity did not deserialize properly'
    assert (transaction.currency_pair is not None), 'Currency pair did not deserialize properly'
    assert (transaction.way is not None), 'Way did not deserialize properly'
    assert (
        transaction.ask_order_id is not None), 'Ask order ID did not deserialize properly'
    assert (
        transaction.bid_order_id is not None), 'Bid order ID did not deserialize properly'


def test_get_currency_pairs():
    """Test currency pairs fetching from REST API"""
    response = GatecoinAPI.get_currency_pairs()
    assert (response is not None), 'Response did not deserialize properly'

    assert (response.response_status is not None), 'Response status does not exist'
    assert (response.currency_pairs is not None), 'Currency pairs list does not exist'

    assert (response.response_status is not None), 'Response status did not deserialize successfully'
    assert (response.currency_pairs is not None), 'Currency pairs list did not deserialize successfully'

    assert (response.response_status.message ==
            'OK'), 'API response not successful'
    assert (len(response.currency_pairs) > 0), 'Empty currency pairs list'

    for currency_pair in response.currency_pairs:
        _test_currency_pair(currency_pair)


def test_get_market_depth():
    """Test fetching market depth info from REST API"""
    response = GatecoinAPI.get_market_depth('BTCUSD')
    assert (response is not None), 'Response did not deserialize properly'

    assert (response.response_status is not None), 'Response status does not exist'
    assert (response.asks is not None), 'Asks list does not exist'
    assert (response.bids is not None), 'Bids list does not exist'

    assert (response.response_status.message ==
            'OK'), 'API response not successful'
    assert (len(response.asks) > 0), 'Empty asks list'
    assert (len(response.bids) > 0), 'Empty bids list'

    for limit in response.asks:
        _test_limit(limit)

    for limit in response.bids:
        _test_limit(limit)


def test_get_order_book():
    """Test fetching order book from REST API"""
    response = GatecoinAPI.get_order_book('BTCUSD')
    assert (response is not None), 'Response did not deserialize properly'

    # Disabled for now, v1 does not return response_status for this method
    # assert (response.response_status.message == 'OK'), 'API response not successful'
    assert (response.asks is not None), 'Asks list does not exist'
    assert (response.bids is not None), 'Bids list does not exist'

    assert (len(response.asks) > 0), 'Empty asks list'
    assert (len(response.bids) > 0), 'Empty bids list'

    for limit in response.asks:
        _test_limit(limit)

    for limit in response.bids:
        _test_limit(limit)


def test_get_recent_transactions():
    """Test fetching recent transactions from REST API"""
    response = GatecoinAPI.get_recent_transactions('BTCUSD')
    assert (response is not None), 'Response did not deserialize properly'

    assert (response.response_status.message ==
            'OK'), 'API response not successful'
    assert (len(response.transactions) > 0), 'Empty transactions list'

    for transaction in response.transactions:
        _test_transaction(transaction)
