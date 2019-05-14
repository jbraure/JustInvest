
from django.forms import ModelForm, ValidationError

from .models import Trade
from .lib.justinvest import finance

class TradeForm(ModelForm):
    def clean_ticker(self):
        ticker_data = self.cleaned_data['ticker']
        if not finance.is_ticker_existing(ticker_data):
            raise ValidationError('This ticker could not be found in Yahoo finance!')
        return ticker_data

    class Meta:
        model = Trade
        fields = [
            'ticker',
            'name',
            'asset_class',
            'currency',
            'trade_date',
            'action',
            'number_of_shares',
            'price_per_share_paid'
        ]
