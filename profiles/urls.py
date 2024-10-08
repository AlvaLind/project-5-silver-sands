from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path(
        'order_history/<order_number>', views.order_history,
        name='order_history'),
    path(
        'add_to_favourites/<int:wine_id>/', views.add_to_favourites,
        name='add_to_favourites'),
    path(
        'remove_from_favourites/<int:wine_id>/', views.remove_from_favourites,
        name='remove_from_favourites'),
    path('favourites/', views.favourites, name='favourites'),
]
