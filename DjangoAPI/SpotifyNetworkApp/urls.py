from django.urls import re_path, path
from .views import UserSignIn, ArtistNetwork
# from .views import index

app_name = 'api'

urlpatterns = [
    path('sign-in', UserSignIn.as_view()),
    path('get-network', ArtistNetwork.as_view()),
]
