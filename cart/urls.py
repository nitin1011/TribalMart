from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view-cart'),
    path('update/<int:pk>', views.update_cart, name='update-cart'),
]