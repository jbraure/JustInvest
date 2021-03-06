"""justinvest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from trades.views import HomeView, TradeListView, HoldingListView
from trades.views import TradeFormView, StockChartView
from trades.views import TradeDetailView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from trades import views

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^trades/$',
        TradeListView.as_view(),
        name='trades'),

    url(r'^holdings/$',
        HoldingListView.as_view(),
        name='holdings'),

    url(r'^trades/create$',
        TradeFormView.as_view(),
        name='create'),

    path(r'trades/<int:pk>/delete/',
    views.TradeDelete.as_view(),
    name='trade_delete'),

    # ex: trades/7/
    url(r'^trades/(?P<trade_id>\d+)/?$',
        TradeDetailView.as_view(),
        name='detail'),

    # ex: stockchart/ZGLD.SW
    url(r'^stockchart/(?P<ticker>\S+)$',
        StockChartView.as_view(),
        name='stockchart'),

    #url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^signup/$', views.signup, name='signup'),

    url(r'^login/$',
        auth_views.LoginView.as_view(),
        kwargs={'next_page': reverse_lazy('home')},
        name='login'),

    url(r'^logout/$',
        auth_views.LogoutView.as_view(),
        name='logout'),

    #ex : /quote/AAPL.json
    url(r'^quote/(?P<ticker>\S+).json$', views.quote),

    url(r'^$', HomeView.as_view(), name='home'),
]
