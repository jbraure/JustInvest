from django.forms import ModelForm
from .models import Trade

class TradeForm(ModelForm):
    class Meta:
        model = Trade
        fields = ['ticker', 'name', 'asset_class', 'currency', 'trade_date', \
            'action', 'number_of_shares', 'price_paid']
# add form validation for ticker name
