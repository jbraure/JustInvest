"""lsltrading URL Configuration

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
from trades.views import HomeView, TradeListView, TradeFormView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^trades/$',
        TradeListView.as_view(),
        name='trades'),

    url(r'^trades/create$',
        TradeFormView.as_view(),
        name='create'),

    url(r'^login/$',
        auth_views.LoginView.as_view(),
        kwargs={'template_name': 'admin/login.html'},
        name='login'),

    url(r'^logout/$',
        auth_views.LogoutView.as_view(),
        kwargs={'next_page': reverse_lazy('home')},
        name='logout'),

    url(r'^$', HomeView.as_view(), name='home'),
]
