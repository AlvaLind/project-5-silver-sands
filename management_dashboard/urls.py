from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:wine_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:wine_id>/', views.delete_product, name='delete_product'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('orders/<int:order_id>/details/', views.order_details, name='order_details'),
]
