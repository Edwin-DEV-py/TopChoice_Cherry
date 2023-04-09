from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_cart, name='shopping_cart'),
    path('add/<int:product_id>/',views.add, name="add"),
    path('remove/<int:product_id>/',views.remove, name="remove"),
    path('delete/<int:product_id>/',views.delete, name="delete"),
    path('shipping_address/',views.shipping_address, name="shipping_address"),
]

