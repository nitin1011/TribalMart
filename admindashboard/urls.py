from django.urls import path
from . import views

urlpatterns = [
    path('user-list', views.user_list, name='user-list'),
    path('user-view/<int:pk>', views.user_view, name='user-view'),
]