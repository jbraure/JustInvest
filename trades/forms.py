from django.forms import ModelForm
from .models import Trade

class TradeForm(ModelForm):
    class Meta:
        model = Trade
        fields = ['ticker', 'currency', 'purchase_date', \
            'number_of_shares', 'price']

    # ticker = models.CharField('Ticker', max_length=20)
    # currency = models.CharField('Currency', max_length=5)
    # purchase_date = models.DateTimeField('Date purchased', auto_now=True)
    # sell_date = models.DateTimeField('Date sold', auto_now=False)
    # number_of_shares = models.IntegerField('Number of shares', default=1)
    # owner = models.EmailField()
    # price = models.FloatField()
