"""API client module for Gatecoin REST API"""

from .request import Request


class GatecoinAPI:

    public_key: str = ''
    private_key: str = ''

    @classmethod
    def set_credentials(cls, private_key: str, public_key: str):
        """Set public and private key credentials for API"""
        cls.private_key = private_key
        cls.public_key = public_key

    @classmethod
    def get_currency_pairs(cls):
        """Get currency pairs"""
        return Request(cls.private_key, cls.public_key, 'v1/Reference/CurrencyPairs').send()

    @classmethod
    def get_market_depth(cls, currency_pair: str):
        """Get currency pair market depth"""
        return Request(cls.private_key, cls.public_key, 'v1/Public/MarketDepth/{0}'.format(currency_pair)).send()
    
    @classmethod
    def get_order_book(cls, currency_pair: str):
        """Get currency pair order book"""
        return Request(cls.private_key, cls.public_key, 'v1/{0}/OrderBook'.format(currency_pair)).send()

    @classmethod
    def get_recent_transactions(cls, currency_pair: str):
        """Get recent transactions for the currency pair"""
        return Request(cls.private_key, cls.public_key, 'v1/Public/Transactions/{0}'.format(currency_pair)).send()

    @classmethod
    def get_balances(cls):
        """Get all balances"""
        return Request(cls.private_key, cls.public_key, 'v1/Balance/Balances').send()
