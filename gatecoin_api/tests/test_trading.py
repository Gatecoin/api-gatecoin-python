"""Test suite for Gatecoin REST API public methods"""
import os

import pytest

from gatecoin_api import GatecoinAPI
from gatecoin_api.constants import BID
from gatecoin_api.types import AccountBalance, OpenOrder, TraderTransaction

# This is used to store one order id that is received
# in the get_open_orders response and is further consumed
# as input to the get_open_order request.
order_id = None


@pytest.fixture
def api() -> GatecoinAPI:
    """Fixture to return API class with credentials set for testing"""
    assert (os.environ.get(
        'GC_TESTS_API_KEY') is not None), 'GC_TESTS_API_KEY not set in environment for trading API\
        tests'
    assert (os.environ.get(
        'GC_TESTS_PUBLIC_KEY') is not None), 'GC_TESTS_PUBLIC_KEY not set in environment for\
        trading API tests'
    GatecoinAPI.set_credentials(os.environ.get(
        'GC_TESTS_API_KEY'), os.environ.get('GC_TESTS_PUBLIC_KEY'))
    return GatecoinAPI


def _test_balance(balance: AccountBalance):
    assert (balance.currency is not None), 'Currency did not deserialize properly'
    assert (balance.balance is not None), 'Balance did not deserialize properly'
    assert (balance.available_balance is not None), 'Available balance did not deserialize properly'
    assert (balance.pending_incoming is not None), 'Pending incoming did not deserialize properly'
    assert (balance.pending_outgoing is not None), 'Pending outgoing did not deserialize properly'
    assert (balance.open_order is not None), 'Open order did not deserialize properly'
    assert (balance.pledging is not None), 'Pledging did not deserialize properly'
    assert (balance.is_digital is not None), 'IsDigital did not deserialize properly'


def _test_trader_transaction(transaction: TraderTransaction):
    assert (transaction.transaction_id is not None), 'Transaction ID did not deserialize properly'
    assert (transaction.transaction_time is not None), 'Transaction time did not deserialize properly'
    assert (
        transaction.ask_order_id is not None), 'Ask order ID did not deserialize properly'
    assert (
        transaction.bid_order_id is not None), 'Bid order ID did not deserialize properly'
    assert (transaction.price is not None), 'Price did not deserialize properly'
    assert (transaction.currency_pair is not None), 'Currency pair did not deserialize properly'
    assert (transaction.way is not None), 'Way did not deserialize properly'
    assert (transaction.fee_roll is not None), 'Fee roll did not deserialize properly'
    assert (transaction.fee_rate is not None), 'Fee rate did not deserialize properly'
    assert (
        transaction.fee_amount is not None), 'Fee amount did not deserialize properly'


def _test_open_order(order: OpenOrder):
    assert (order.code is not None), 'Order code did not deserialize properly'
    assert (order.cl_order_id is not None), 'CL Order ID did not deserialize properly'
    assert (order.side is not None), 'Side did not deserialize properly'
    assert (order.price is not None), 'Price did not deserialize properly'
    assert (order.initial_quantity is not None), 'Initial quantity did not deserialize properly'
    assert (order.remaining_quantity is not None), 'Remaining quantity did not deserialize properly'
    assert (order.status is not None), 'Order status did not deserialize properly'
    assert (order.status_desc is not None), 'Order status description did not deserialize properly'
    
    # This is none for all new orders
    # assert (order.transaction_sequence_number is not None), 'Transaction sequence number did not deserialize properly'
    assert (order.type is not None), 'Order type did not deserialize properly'
    assert (order.date is not None), 'Order date did not deserialize properly'
    
    # This is none for all new orders
    # assert (order.trades is not None), 'Order trades did not deserialize properly'


def test_get_balances(api: GatecoinAPI):
    """Test fetching currency balances from REST API"""
    response = api.get_balances()
    assert (response is not None), 'Response did not deserialize properly'

    assert (response.response_status is not None), 'Response status does not exist'
    assert (response.response_status.message ==
            'OK'), 'API response not successful'

    assert (response.balances is not None), 'Balances list did not deserialize properly'
    assert (len(response.balances) > 0), 'Empty balances list'

    for balance in response.balances:
        _test_balance(balance)


def test_get_balance(api: GatecoinAPI):
    """Test USD currency balance from REST API"""
    response = api.get_balance('USD')
    assert (response is not None), 'Response did not deserialize properly'

    assert (response.response_status is not None), 'Response status does not exist'
    assert (response.response_status.message ==
            'OK'), 'API response not successful'

    assert (response.balance is not None), 'Balance was not included in response'

    _test_balance(response.balance)


def test_create_order(api: GatecoinAPI):
    """Test create a dummy order for BTC using USD"""
    response = api.create_order('BTCUSD', BID, 0.1, 0.1)
    assert (response is not None), 'Response did not deserialize properly'

    assert (response.response_status is not None), 'Response status does not exist'
    assert (response.response_status.message ==
            'OK'), 'API response not successful'
    assert (response.cl_order_id is not None), 'Cl Order Id was not included in response'

    global order_id
    order_id = response.cl_order_id
    print(order_id)


def test_get_open_orders(api: GatecoinAPI):
    """Test fetching all open orders from REST API"""
    global order_id
    response = api.get_open_orders()
    assert (response is not None), 'Response did not deserialize properly'

    assert (response.response_status is not None), 'Response status does not exist'
    assert (response.response_status.message ==
            'OK'), 'API response not successful'

    assert (response.orders is not None), 'Orders were not included in response'

    for order in response.orders:
        _test_open_order(order)
        order_id = response.orders[0].cl_order_id


def test_get_open_order(api: GatecoinAPI):
    """Test fetching specific open order from REST API"""
    global order_id

    # Make sure to test only if a valid order id is available
    if order_id is not None:
        response = api.get_open_order(order_id)

        assert (response is not None), 'Response did not deserialize properly'

        assert (response.response_status is not None), 'Response status does not exist'
        assert (response.response_status.message ==
                'OK'), 'API response not successful'

        assert (response.order is not None), 'Order was not included in response'

        _test_open_order(response.order)


def test_cancel_order(api: GatecoinAPI):
    """Test cancelling the order created in the previous test"""
    if order_id is not None:
        response = api.cancel_order(order_id)
        assert (response is not None), 'Response did not deserialize properly'

        assert (response.response_status is not None), 'Response status does not exist'
        assert (response.response_status.message ==
                'OK'), 'API response not successful'


def test_cancel_all_orders(api: GatecoinAPI):
    """Test cancelling all open orders"""
    response = api.cancel_all_orders()
    assert (response is not None), 'Response did not deserialize properly'

    assert (response.response_status is not None), 'Response status does not exist'
    assert (response.response_status.message ==
            'OK'), 'API response not successful'
