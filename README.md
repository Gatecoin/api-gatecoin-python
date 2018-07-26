# Gatecoin Python REST API client

This is a simple Gatecoin python REST API client library that abstracts away the REST for the end user.

## Installation

The library can be collected from PyPI like so:

`$ pip install gate_coin`

## Usage

The package exposes the `GatecoinAPI` class which has methods from the Gatecoin REST API. Public methods may be directly used, for trading methods API credentials need to be set:

`GatecoinAPI.set_credentials('api_key', 'public_key')`

after that trading APIs may be used, for example:

`GatecoinAPI.get_balances()`

## Implemented methods
- Trading
  - set_credentials
  - get_balances
- Public
  - get_currency_pairs
  - get_market_depth
  - get_order_book
  - get_recent_transactions
