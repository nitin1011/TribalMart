from django.urls import path
from . import views

urlpatterns = [
    path('register', views.complaint_register, name='complaint'),
    path('list', views.complaint_list, name='complaint-list'),
    path('view/<int:pk>', views.complaint_view, name='complaint-view'),
    path('reply/<int:pk>', views.reply, name='complaint-reply'),
]