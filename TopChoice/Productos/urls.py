from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.store,name="store"),
    path('<slug:category_slug>',views.store, name='product_x_category')
]