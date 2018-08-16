# Gatecoin Python REST API client

This is a simple Gatecoin python REST API client library that abstracts away the REST for the end user.

## Installation

The library can be collected from PyPI like so:

`$ pip install gatecoin_api`

## Usage

The package exposes the `GatecoinAPI` class which has methods from the Gatecoin REST API. Public methods may be directly used, for trading methods API credentials need to be set:

`GatecoinAPI.set_credentials('api_key', 'public_key')`

After that trading APIs may be used. Example usage of the Public API:

```python
res = GatecoinAPI.get_currency_pairs()
print(res.response_status.message) # 'OK'
print(res.currency_pairs[0].trading_code) # 'BTCEUR'
print(res.currency_pairs[0].base_currency) # 'BTC'
print(res.currency_pairs[0].price_decimal_places) # 1
```

## Implemented methods
- Trading
  - set_credentials
  - get_balances
  - get_balance
  - get_open_orders
  - get_open_order
  - create_order
  - cancel_order
  - cancel_all_orders
  - get_trade_history
- Public
  - get_currency_pairs
  - get_market_depth
  - get_order_book
  - get_recent_transactions

## Development

To develop or test using this package without installing from PyPI, you can clone the repository and set up the environment in a virtual envirnonment at the root of the working copy:

`$ virtualenv venv --python=python3`

Activate the virtual environment:

`$ source venv/bin/activate`

Install development dependencies:

`$ pip install -r requirements.txt`

Run the interactive python shell and you can use the package as the example given below:

```python
$ python
>>> from gatecoin_api import GatecoinAPI as GA
>>> res = GA.get_currency_pairs()
>>> res.response_status.message
'OK'
>>> res.currency_pairs[0].trading_code
'BTCEUR'
>>> res.currency_pairs[0].base_currency
'BTC'
>>> res.currency_pairs[0].quote_currency
'EUR'
>>> res.currency_pairs[0].display_name
'BTC / EUR'
>>> res.currency_pairs[0].name
'BTC / EUR'
>>> res.currency_pairs[0].price_decimal_places
1
```

## Tests

To setup correctly for tests, set valid development API keys and API base URL in your shell environment:

```sh
export GTC_TESTS_PRIVATE_KEY=<PRIVATE_KEY>
export GTC_TESTS_PUBLIC_KEY=<PUBLIC_KEY>
export GTC_API_BASE_URL=<API_BASE_KEY>
```

For Windows command line, please use the `set` command:

```bat
set GTC_TESTS_PRIVATE_KEY=<PRIVATE_KEY>
set GTC_TESTS_PUBLIC_KEY=<PUBLIC_KEY>
set GTC_API_BASE_URL=<API_BASE_KEY>
```

 To run tests please execute:

`$ python setup.py test`

If development keys are not set, trading scope tests will fail.