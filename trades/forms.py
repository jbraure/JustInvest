from django.forms import ModelForm
from .models import Trade

class TradeForm(ModelForm):
    class Meta:
        model = Trade
        fields = ['ticker', 'currency', 'purchase_date', \
            'number_of_shares', 'price_paid']
