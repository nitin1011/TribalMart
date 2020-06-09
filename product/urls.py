from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_product, name='add-product'),
    path('all-product', views.all_product, name='all-product'),
    path('detail/<int:pk>', views.product_detail, name='product-detail'),
    path('edit/<int:pk>', views.edit_product, name='edit-product'),
    path('delete/<int:pk>', views.delete_product, name='delete-product'),
    path('review/<int:pk>', views.review, name='review'),
]