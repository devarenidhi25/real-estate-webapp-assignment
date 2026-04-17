"""
realestate/urls.py

URL configuration for realestate app.
"""

from django.urls import path
from .views import query_view, top_growth_view

urlpatterns = [
    path('query/', query_view, name='query'),
    path('top-growth/', top_growth_view, name='top_growth'),
]