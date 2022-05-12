from django.urls import path
from .views import NameViews

urlpatterns = [
    path('api/', NameViews.as_view())
]