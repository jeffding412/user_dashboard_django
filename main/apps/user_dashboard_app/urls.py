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
    url(r'^createNewUser$', views.create_new_user),
    url(r'^delete(?P<id>\d+)$', views.delete_user),
    url(r'^users/edit$', views.edit_profile),
    url(r'^editInfo$', views.edit_information),
    url(r'^editInfo/(?P<id>\d+)$', views.edit_information),
    url(r'^changePassword$', views.change_password),
    url(r'^changePassword/(?P<id>\d+)$', views.change_password),
    url(r'^editDescription$', views.edit_description),
    url(r'^dashboard$', views.dashboard),
    url(r'^returnToDashboard$', views.return_to_dashboard),
    url(r'^users/edit/(?P<id>\d+)$', views.edit_user)
]