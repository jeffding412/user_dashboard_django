from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^loginUser$', views.login_user),
    url(r'^register$', views.register),
    url(r'^registerUser$', views.register_user)
]