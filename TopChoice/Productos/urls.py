from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.store,name="store"),
    path('<slug:category_slug>',views.store, name='product_per_category'),
    path('<slug:category_slug>/<slug:product_slug>',views.product_information,name='product_information'),
]