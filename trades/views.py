# from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
# from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView, FormView
from django.http import HttpResponse, JsonResponse

from .models import Trade
from .forms import TradeForm


import pandas as pd
from datetime import date, timedelta
from pandas_datareader.data import DataReader

class HomeView(TemplateView):
    template_name = 'trades/home.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class TradeListView(TemplateView):
    template_name = 'trades/list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        trades = Trade.objects \
            .filter(user=request.user) \
            .order_by('-purchase_date')
        self.update_values(trades)
        context['trades'] = list(trades)
        return self.render_to_response(context)

    def update_values(self, trades):
        """
        Updates values on the Trade objects
        - Gets current (last close) price
        """
        start_date = date.today() - timedelta(4)
        for trade in trades:
            stock_data = DataReader(trade.ticker, 'yahoo', start=start_date)
            # last close price
            last_close = float(stock_data.tail(1)['Close'])
            trade.current_price = last_close
            # current asset values
            trade.total_value = trade.number_of_shares * last_close
            trade.save()


class TradeFormView(SuccessMessageMixin, FormView):
    template_name = 'trades/create.html'
    form_class = TradeForm
    success_url = reverse_lazy('trades')
    success_message = "Entry was created successfully"

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        return super(TradeFormView, self).get(request, *args, **kwargs)

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def post(self, request, *args, **kwargs):
        return super(TradeFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self._save_with_user(form)
        return super(TradeFormView, self).form_valid(form)

    def _save_with_user(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

# ex: /trades/3/
# url(r'^trades/<int:trade_id>', views.trade_id),
def trade_id(request, trade_id):
    print('OPEN TRADE NUMBER',trade_id)
    return HttpResponse(trade_id)

# TODO move this elsewhere
def is_ticker_existing(ticker):
    try:
        DataReader(ticker, 'yahoo', start=date(2019,1,1))
        return True
    except:
        return False

class StockChartView(TemplateView):
    template_name = 'trades/stockchart.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        ticker = context['ticker']
        if not is_ticker_existing(ticker):
            context['error_message'] = 'No data could be found for ticker ' + ticker
        return self.render_to_response(context)

# TODO move this elsewhere
def index_to_unix(row):
    row.unix = row.unix.value // 10**6
    return row

def quote(request, ticker):
    """
    Returns a JSON response with quote values for requested ticker.
    See https://docs.djangoproject.com/en/2.2/ref/request-response/
    look at highstock json aapl example :
    https://www.highcharts.com/samples/data/aapl-c.json
    https://www.highcharts.com/samples/data/aapl-ohlcv.json
    => date is in epoch format! ex:   1556890200000
    """
    # it seems to work well with this date...
    start_date = date(2017,1,1)
    stock_data_df = DataReader(ticker, 'yahoo', start=start_date)
    # add a column in unix timestamp format
    stock_data_df['unix'] = stock_data_df.index
    stock_data_df = stock_data_df.apply(index_to_unix, axis='columns')
    values_list = stock_data_df.loc[:,['unix', 'Open', 'High', 'Low', 'Close', 'Volume']].values.tolist()
    return JsonResponse(values_list, safe=False)
