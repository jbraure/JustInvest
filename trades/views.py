# Third party imports
from pandas_datareader.data import DataReader
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView, FormView
from django.http import HttpResponse, JsonResponse

# Local application imports
from .models import Trade
from .forms import TradeForm
from .lib.justinvest import finance


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
            .order_by('-trade_date')
        self.update_values(trades)
        context['trades'] = list(trades)
        return self.render_to_response(context)

    def update_values(self, trades):
        """
        Updates values on the Trade objects : current (last close) price,
        positivity (value raised)
        """
        for trade in trades:
            last_close = finance.get_last_close(trade.ticker)
            trade.current_price = last_close
            # current asset values
            trade.total_value = trade.number_of_shares * last_close
            trade.positive = trade.price_paid < trade.current_price
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

class TradeDetailView(TemplateView):
    template_name = 'trades/trade.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # load trade with id
        trade_id = context['trade_id']
        trade = Trade.objects.get(pk=trade_id)
        context['trade'] = trade
        context['buy_year'] = trade.trade_date.year
        context['buy_month'] = trade.trade_date.month-1
        context['buy_day'] = trade.trade_date.day
        if trade.currency == 'USD':
            context['total_value_in_chf'] = finance.usd_to_chf(trade.total_value)
        else:
            if trade.currency == 'EUR':
                context['total_value_in_chf'] = finance.eur_to_chf(trade.total_value)
        return self.render_to_response(context)

class StockChartView(TemplateView):
    template_name = 'trades/stockchart.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        ticker = context['ticker']
        if not finance.is_ticker_existing(ticker):
            context['error_message'] = 'No data could be found for ticker ' + ticker
        return self.render_to_response(context)



def quote(request, ticker):
    """
    Returns a JSON response with quote values for requested ticker.
    See https://docs.djangoproject.com/en/2.2/ref/request-response/
    look at highstock json aapl example :
    https://www.highcharts.com/samples/data/aapl-c.json
    https://www.highcharts.com/samples/data/aapl-ohlcv.json
    => date is in epoch format! ex:   1556890200000
    """
    values_list = finance.get_ohlc_quote(ticker)
    return JsonResponse(values_list, safe=False)
