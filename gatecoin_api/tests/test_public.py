"""Test suite for Gatecoin REST API public methods"""
import pytest
from gatecoin_api import GatecoinAPI


def test_get_currency_pairs():
    """Test currency pairs fetching from REST API"""
    response = GatecoinAPI.get_currency_pairs()
    assert (response is not None), 'Response did not deserialize properly'


def test_get_market_depth():
    """Test fetching market depth info from REST API"""
    response = GatecoinAPI.get_market_depth('BTCUSD')
    assert (response is not None), 'Response did not deserialize properly'


def test_get_order_book():
    """Test fetching order book from REST API"""
    response = GatecoinAPI.get_order_book('BTCUSD')
    assert (response is not None), 'Response did not deserialize properly'


def test_get_recent_transactions():
    """Test fetching recent transactions from REST API"""
    response = GatecoinAPI.get_recent_transactions('BTCUSD')
    assert (response is not None), 'Response did not deserialize properly'
