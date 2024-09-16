from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('our_story/', views.about_us, name='about_us'),
]
