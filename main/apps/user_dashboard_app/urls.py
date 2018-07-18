from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^loginUser$', views.login_user),
    url(r'^register$', views.register),
    url(r'^registerUser$', views.register_user),
    url(r'^dashboard/admin$', views.admin),
    url(r'^logoff$', views.logoff),
    url(r'^users/new$', views.new_user),
    url(r'^createNewUser$', views.create_new_user)
    # url(r'^users/edit/(?P<id>\d+))', views.edit_user)
]