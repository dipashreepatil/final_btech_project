from django.conf.urls import  url

from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('search_query/',views.investorsearch, name='search_view_investor'),
    path('numerical_predictions', views.investor_numeric_prediction, name="numerical_prediction_investor"),
    path('recommendations' , views.recommendation , name = "recommendations"),
     ]
