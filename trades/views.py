from decimal import Decimal as D

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
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, JsonResponse

# Local application imports
from .models import Trade, HoldingManager, Holding
from .forms import TradeForm
from .lib.justinvest import finance


class HomeView(TemplateView):
    """ View used to display the PORTFOLIO globally with plots.
    """
    template_name = 'trades/home.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class HoldingListView(TemplateView):
    """ View used to display the holdings.
    """
    template_name = 'trades/holding_list.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        holdings = Holding.objects \
            .filter(user=request.user) \
            .order_by('asset_class')
        context['holdings'] = list(holdings)
        return self.render_to_response(context)

class TradeListView(TemplateView):
    """ View used to display the TRADES list.
    """
    template_name = 'trades/trade_list.html'

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
        """ Updates values on the Trade objects : current (last close) price,
            positivity (value raised)
        """
        for trade in trades:
            last_close = finance.get_last_close(trade.ticker)
            trade.current_price = last_close
            # current asset values
            trade.total_value = D(trade.number_of_shares * last_close)
            trade.positive = trade.price_per_share_paid < trade.current_price
            trade.save()


class TradeFormView(SuccessMessageMixin, FormView):
    """ View used to ENTER NEW TRADES
    """
    template_name = 'trades/create.html'
    form_class = TradeForm
    success_url = reverse_lazy('trades')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        return super(TradeFormView, self).get(request, *args, **kwargs)

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def post(self, request, *args, **kwargs):
        return super(TradeFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self._save_with_user(form)
        return super(TradeFormView, self).form_valid(form)

    def create_or_update_holding_on_buy(self, trade):
        holdings = Holding.objects.filter(user=trade.user, ticker=trade.ticker)
        holding = holdings.first()

        if holding is None:
            # when not existing : create
            Holding.objects.create_holding(trade.user, trade.ticker,
                trade.name, trade.asset_class,
                trade.currency, trade.number_of_shares)
        else:
            # else update (increment) holding count
            holding.number_of_shares += trade.number_of_shares
            holding.save()

    def create_or_update_holding_on_sell(self, trade):
        holdings = Holding.objects.filter(user=trade.user, ticker=trade.ticker)
        holding = holdings.first()

        if holding is None:
            # when not existing : create
            # TODO error message
            print('ERROR : CANNOT SELL A HOLDING NOT FOUND')
        else:
            # else update (decrement) holding count
            holding.number_of_shares -= trade.number_of_shares
            holding.save()

    def _save_with_user(self, form):
        self.object = form.save(commit=False)
        trade = self.object
        trade.user = self.request.user
        if trade.is_buy():
            self.create_or_update_holding_on_buy(trade)
        else:
            self.create_or_update_holding_on_sell(trade)

        trade.save()



class TradeDelete(DeleteView):
    model = Trade
    success_url = reverse_lazy('trades')

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
            context['total_value_in_chf'] = D(finance.usd_to_chf(trade.total_value))
        else:
            if trade.currency == 'EUR':
                context['total_value_in_chf'] = D(finance.eur_to_chf(trade.total_value))
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
