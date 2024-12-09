from django.urls import path
from . import views
from .api import views as api_views

urlpatterns = [
    path('rankings/', views.rankings, name='rankings'),
    path('rankings/download/', views.download_rankings_csv, name='download_rankings'),
    path('api/set_class', api_views.set_class, name='set_class'),
]