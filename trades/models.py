import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

CURRENCIES = (
    ('CHF', 'CHF : Swiss Franc'),
    ('EUR', 'EUR : Euro'),
    ('USD', 'USD : US Dollar'),
 )

ACTIONS = (
    ('BUY', 'Buy'),
    ('SELL', 'Sell'),
 )

ASSET_CLASSES = (
    ('STOCK', 'Stock'),
    ('GOLD', 'Gold'),
    ('CASH', 'Cash'),
    ('LONG_BONDS', 'Long-term bonds'),
    ('MED_BONDS', 'Medium-term bonds'),
    ('SHORT_BONDS', 'Short-term bonds'),
    ('CRYPTO', 'Cryptocurrencies'),
    ('OTHER', 'Other'),
)

class Trade(models.Model):
    """
    Class representing a buy or sell action.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0')
    ticker = models.CharField('Ticker', max_length=20, default='AAPL')
    name = models.CharField('Name', max_length=50, default='Apple')
    asset_class = models.CharField('Asset class', max_length=50, default='STOCK', choices=ASSET_CLASSES)
    currency = models.CharField('Currency', max_length=3, default='USD', choices=CURRENCIES)
    action = models.CharField('Action', max_length=4, default='BUY', choices=ACTIONS)
    trade_date = models.DateTimeField('Date', default=timezone.now)
    number_of_shares = models.FloatField('Number of shares', default=1)
    price_per_share_paid = models.DecimalField('Price paid (per share) in asset currency', decimal_places=2, max_digits=10)
    current_price = models.DecimalField('Last close value', decimal_places=2, max_digits=10, default=0)
    total_value = models.DecimalField('Total value', decimal_places=2, max_digits=10, default=0)
    positive = models.BooleanField('positive', default=False)

    def __str__(self):
        return self.ticker

    def get_current_price_str(self):
        return '{:8.2f}'.format(self.current_price)

    def get_total_value_str(self):
        return '{:8.2f}'.format(self.total_value)

    def is_buy(self):
        return self.action == 'BUY'


class HoldingManager(models.Manager):
    """ Class used to create holdings.
        See doc:
        https://docs.djangoproject.com/en/2.2/ref/models/instances/
    """
    def create_holding(self, user, ticker, name,
        asset_class, currency, number_of_shares):
        holding = self.create(
            user = user,
            ticker = ticker,
            name = name,
            asset_class = asset_class,
            currency = currency,
            number_of_shares = number_of_shares)
        return holding

class Holding(models.Model):
    """
    Class representing an asset hold in the portfolio. Holdings will mostly
    be updated, when new shares are bought or sold upon rebalancing.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0')
    ticker = models.CharField('Ticker', max_length=20, default='AAPL')
    name = models.CharField('Name', max_length=50, default='Apple')
    asset_class = models.CharField('Asset class', max_length=50, default='STOCK', choices=ASSET_CLASSES)
    currency = models.CharField('Currency', max_length=3, default='USD', choices=CURRENCIES)
    number_of_shares = models.FloatField('Number of shares', default=1)
    # See HoldingManager
    objects = HoldingManager()


class BalanceHistory(models.Model):
    """
    Class representing an item of portfolio balance history,
    typically one item per day will be stored to monitor the
    portfolio performance.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0')
    total_value_chf = models.DecimalField('Total value in CHF', decimal_places=2, max_digits=10, default=0)
    date = models.DateField('Date', default=timezone.now)
