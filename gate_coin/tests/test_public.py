"""Test suite for Gatecoin REST API public methods"""
import pytest
from gate_coin import GatecoinAPI


def check_response(response):
    """Utility method to verify returned response is successful"""
    assert ('responseStatus' in response), 'Status missing in response'
    assert ('message' in response['responseStatus']
            ), 'Status message missing in response'
    assert('OK' == response['responseStatus']['message']
           ), 'Status message does not indicate success'


def test_get_currency_pairs():
    """Test currency pairs fetching from REST API"""
    response = GatecoinAPI.get_currency_pairs()
    check_response(response)
    assert ('currencyPairs' in response), 'Currency pairs missing in response'
    assert (type(response['currencyPairs'])
            is list), 'Currency pairs is not a list'
    assert (len(response['currencyPairs']) > 0), 'Empty currency pairs list'

    for currency_pair in response['currencyPairs']:
        assert('tradingCode' in currency_pair and type(
            currency_pair['tradingCode']) is str), 'Trading code missing or wrong type in currency pair'
        assert('baseCurrency' in currency_pair and type(
            currency_pair['baseCurrency']) is str), 'Base currency missing or wrong type in currency pair'
        assert('quoteCurrency' in currency_pair and type(
            currency_pair['quoteCurrency']) is str), 'Quote currency missing or wrong type in currency pair'
        assert ('displayName' in currency_pair and type(
            currency_pair['displayName']) is str), 'Display name missing or wrong type in currency pair'
        assert('priceDecimalPlaces' in currency_pair and type(
            currency_pair['priceDecimalPlaces']) is int), 'Price decimal places missing or wrong type in currency pair'
        assert('name' in currency_pair and type(
            currency_pair['name']) is str), 'Name missing or wrong type in currency pair'


def test_get_market_depth():
    """Test fetching market depth info from REST API"""
    response = GatecoinAPI.get_market_depth('BTCUSD')
    check_response(response)

    assert ('asks' in response), 'Asks missing in response'
    assert (type(response['asks']) is list), 'Asks is not a list'

    for ask in response['asks']:
        assert('price' in ask and (type(ask['price']) is float or type(
            ask['price']) is int)), 'Price missing or wrong type in asking order'
        assert('volume' in ask and (type(ask['volume']) is float or type(
            ask['volume']) is int)), 'Volume missing or wrong type in asking order'

    assert ('bids' in response), 'Bids missing in response'
    assert (type(response['bids']) is list), 'Bids is not a list'

    for bid in response['bids']:
        assert('price' in bid and (type(bid['price']) is float or type(
            bid['price']) is int)), 'Price missing or wrong type in bidding order'
        assert ('volume' in bid and (type(bid['volume']) is float or type(
            bid['volume']) is int)), 'Volume missing or wrong type in bidding order'

def test_get_order_book():
    """Test fetching order book from REST API"""
    response = GatecoinAPI.get_order_book('BTCUSD')

    assert ('asks' in response), 'Asks missing in response'
    assert (type(response['asks']) is list), 'Asks is not a list'

    for ask in response['asks']:
        assert(len(ask) == 2), 'Asking order length mismatch'
        assert((type(ask[0]) is float or type(ask[0]) is int)
                ), 'Price missing or wrong type in asking order'
        assert((type(ask[1]) is float or type(ask[1]) is int)
                ), 'Volume missing or wrong type in asking order'

    assert ('bids' in response), 'Bids missing in response'
    assert (type(response['bids']) is list), 'Bids is not a list'

    for bid in response['bids']:
        assert(len(bid) == 2), 'Bidding order length mismatch'
        assert((type(bid[0]) is float or type(bid[0]) is int)
                ), 'Price missing or wrong type in bidding order'
        assert ((type(bid[1]) is float or type(bid[1]) is int)
                ), 'Volume missing or wrong type in bidding order'

def test_get_recent_transactions():
    """Test fetching recent transactions from REST API"""
    response = GatecoinAPI.get_recent_transactions('BTCUSD')
    check_response(response)

    assert ('transactions' in response), 'Transactions missing in response'
    assert (type(response['transactions'])
            is list), 'Transactions is not a list'

    for transaction in response['transactions']:
        assert('transactionId' in transaction and type(
            transaction['transactionId']) is int), 'Transaction ID missing or wrong type in transaction'
        assert('transactionTime' in transaction and type(transaction['transactionTime']) is str and int(
            transaction['transactionTime'])), 'Transaction timestamp missing or wrong type in transaction'
        assert('transactionId' in transaction and type(
            transaction['transactionId']) is int), 'Transaction ID missing or wrong type in transaction'
        assert('price' in transaction and (type(transaction['price']) is float or type(
            transaction['price']) is int)), 'Price missing or wrong type in transaction'
        assert ('quantity' in transaction and (type(transaction['quantity']) is float or type(
            transaction['quantity']) is int)), 'Quantity missing or wrong type in transaction'
        assert ('currencyPair' in transaction and type(
            transaction['currencyPair']) is str), 'Currency pair missing or wrong type in transaction'
        assert ('way' in transaction and type(
            transaction['way']) is str), 'Way missing or wrong type in transaction'
        assert('askOrderId' in transaction and type(
            transaction['askOrderId']) is str), 'Asking order ID missing or wrong type in transaction'
        assert('bidOrderId' in transaction and type(
            transaction['bidOrderId']) is str), 'Bidding order ID missing or wrong type in transaction'
