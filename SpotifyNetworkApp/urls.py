from django.urls import re_path
from SpotifyNetworkApp import views

urlpatterns = [
    re_path(r'^users/$', views.usersApi),
    re_path(r'^users/([0-9]+)$', views.usersApi),
    re_path(r'^artists/$', views.artistsApi),
    re_path(r'^artists/([0-9]+)$', views.artistsApi)
]
