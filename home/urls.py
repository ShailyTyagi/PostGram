from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from .models import *


app_name = 'home'
urlpatterns = [

    url(r'^index/$', views.UserRegisterView.as_view(), name='register'),

    url(r'^post/$', views.PostView.as_view(), kwargs=dict(model=User), name='post'),

    url(r'^(?P<user_id>[0-9]+)/feed/$', views.feedview, name='feed'),

    url(r'^login/$', views.UserLoginView.as_view(), name='login'),

    url(r'^logout/$', auth_views.LogoutView.as_view(), {'template_name': 'home/login.html'}, name='logout'),

    url(r'^search/$', include('haystack.urls'), name='search'),

    url(r'^(?P<user_id>[0-9]+)/follow/$', views.followUser, name='followUser'),

    url(r'^(?P<feedmodel_id>[0-9]+)/like/$', views.likeview,  name='like'),

    url(r'^(?P<pk>[0-9]+)/account/$', views.AccountView.as_view(), name='account')



]