from django.urls import re_path, path
from SpotifyNetworkApp import views
# from .views import index

app_name = 'spotifynetworkapp'

urlpatterns = [
    re_path(r'^users/$', views.usersApi),
    re_path(r'^users/([0-9]+)$', views.usersApi),
    re_path(r'^artists/$', views.artistsApi),
    re_path(r'^artists/([0-9]+)$', views.artistsApi),
    re_path(r'^artistassocs/$', views.artistassocsApi),
    re_path(r'^artistassocs/([0-9]+)$', views.artistassocsApi)
]
