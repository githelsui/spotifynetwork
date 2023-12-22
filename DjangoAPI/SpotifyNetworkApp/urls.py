from django.urls import re_path, path
from .views import UserSignIn
# from .views import index

app_name = 'api'

urlpatterns = [
    path('sign-in', UserSignIn.as_view()),
]
