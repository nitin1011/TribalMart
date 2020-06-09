from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('otp', views.verify_otp, name='otp'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.view_profile, name='view-profile'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('change-password', views.change_password, name='change-password'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('account/reset/<str:token>', views.reset_password, name='reset-password'),
    path('search', views.search, name='search-product'),
]