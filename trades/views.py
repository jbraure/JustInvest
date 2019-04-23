# from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView

from .models import Trade


class HomeView(TemplateView):
    template_name = 'trades/home.html'

    @method_decorator(
        login_required(login_url=reverse_lazy('login')))
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
