from django.urls import path
from .views import CloudPublisher

urlpatterns = [
    path('publish-message', CloudPublisher.as_view())
]
