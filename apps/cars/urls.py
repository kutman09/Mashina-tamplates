from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.CarListView.as_view(), name='list'),
    path('add/', views.AddCarView.as_view(), name='add'),
    path('ajax/models/', views.GetModelsView.as_view(), name='ajax_models'),
    path('ajax/favorite/', views.ToggleFavoriteView.as_view(), name='ajax_favorite'),
    path('<slug:slug>/', views.CarDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', views.EditCarView.as_view(), name='edit'),
    path('<slug:slug>/delete/', views.DeleteCarView.as_view(), name='delete'),
]
