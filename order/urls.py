from django.urls import path
from . import views

urlpatterns = [
    path('checkout', views.checkout, name='checkout'),
    path('list', views.order_list, name='order-list'),
    path('view/<int:pk>', views.order_view, name='order-view'),
    path('canceled/<int:pk>', views.canceled, name='canceled'),
    path('finished/<int:pk>', views.finished, name='finished'),
]