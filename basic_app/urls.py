from django.conf.urls import  url

from django.views.generic import TemplateView
from django.urls import path
from basic_app import views


urlpatterns = [
    path('',views.home, name='home'),
    path("login/", views.user_login, name="login"),
    path("signup/",views.user_signup,name="signup"),
    path("contactUs/", views.contactUs),
    path("userGuide/",views.userGuide),
    path("logout/",views.user_logout),
    #path("news/",views.news,name="news"),
    # path('fire', views.fireupdates,name="fireupdates"),
    #path('nifty50', views.Nifty_table,name="nifty50"),

    ]



   