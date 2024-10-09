from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:wine_id>/', views.product_details, name='product_details'),
    path(
        '<int:wine_id>/review/<int:review_id>/delete/', views.delete_review,
        name='delete_review'),
    path(
        '<int:wine_id>/review/<int:review_id>/edit/', views.edit_review,
        name='edit_review'),
    path('search/', views.search_products, name='search_products'),
]
