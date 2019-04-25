import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0')
    ticker = models.CharField('Ticker', max_length=20)
    currency = models.CharField('Currency', max_length=5)
    purchase_date = models.DateTimeField('Date purchased', default=timezone.now)
    sell_date = models.DateTimeField('Date sold', auto_now=False, default=None, blank=True, null=True)
    number_of_shares = models.IntegerField('Number of shares', default=1)
    price_paid = models.FloatField('Price paid')
    current_price = models.FloatField('Current price')
    total_value = models.FloatField('Total value')    

    def __str__(self):
        return self.ticker + ' ' + purchase_date
