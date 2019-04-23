# from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
from django.views import generic
# from django.utils import timezone

from .models import Trade


class IndexView(generic.ListView):
    template_name = 'trades/index.html'
    context_object_name = 'trades_list'

    def get_queryset(self):
        """Return the trades"""
        return Trade.objects.all()
