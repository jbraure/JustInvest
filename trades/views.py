# from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Trade


class HomeView(generic.ListView):
    template_name = 'trades/home.html'
    context_object_name = 'trades_list'

    # @method_decorator(
    #     login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
