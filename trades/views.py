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
from django.http import HttpResponse

from .models import Trade
from .forms import TradeForm


import pandas as pd
from datetime import date, timedelta
from pandas_datareader.data import DataReader

class HomeView(TemplateView):
    template_name = 'trades/home.html'

    @method_decorator(
        login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class TradeListView(TemplateView):
    template_name = 'trades/list.html'

    @method_decorator(
        login_required(login_url=reverse_lazy('login')))
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
        Updates values on the Trades objects
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


class TradeFormView(SuccessMessageMixin, FormView):
    template_name = 'trades/create.html'
    form_class = TradeForm
    success_url = reverse_lazy('trades')
    success_message = "Entry was created successfully"

    @method_decorator(
        login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        return super(TradeFormView, self).get(request, *args, **kwargs)

    @method_decorator(
        login_required(login_url=reverse_lazy('login')))
    def post(self, request, *args, **kwargs):
        return super(TradeFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self._save_with_user(form)
        return super(TradeFormView, self).form_valid(form)

    def _save_with_user(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

def trade_id(request, trade_id):
    print('OPEN TRADE NUMBER',trade_id)
    return HttpResponse(trade_id)
# url(r'^trades/<int:trade_id>',
#         views.trade_id),
