from django.urls import path
from .views import favorites_list

app_name = 'favorites'

urlpatterns = [
    path('', favorites_list, name='list'),
]
