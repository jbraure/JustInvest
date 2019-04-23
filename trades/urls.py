from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # args : route, view, name

    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
]
