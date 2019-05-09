import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

CURRENCIES = (
    ('CHF', 'CHF : Swiss Franc'),
    ('EUR', 'EUR : Euro'),
    ('USD', 'USD : US Dollar'),
 )

class Trade(models.Model):
    """
    Class representing a bought asset. Can be a stock, an ETF, etc.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0')
    ticker = models.CharField('Ticker', max_length=20, default='AAPL')
    name = models.CharField('Name', max_length=50, default='Apple')
    asset_class = models.CharField('Asset class', max_length=50, default='Stock')
    currency = models.CharField('Currency', max_length=5, default='USD', choices=CURRENCIES)
    purchase_date = models.DateTimeField('Date purchased', default=timezone.now)
    number_of_shares = models.IntegerField('Number of shares', default=1)
    price_paid = models.FloatField('Price paid')
    current_price = models.FloatField('Last close value', default=0)
    total_value = models.FloatField('Total value', default=0)
    positive = models.BooleanField('positive', default=False)

    def __str__(self):
        return self.ticker

    def get_current_price_str(self):
        return '{:8.2f}'.format(self.current_price)

    def get_total_value_str(self):
        return '{:8.2f}'.format(self.total_value)

class BalanceHistory(models.Model):
    """
    Class representing an item of portfolio balance history,
    typically one item a day will be stored.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0')
    total_value_chf = models.FloatField('Total value in CHF', default=0)
    date = models.DateField('Date purchased', default=timezone.now)
