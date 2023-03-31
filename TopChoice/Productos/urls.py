from django.urls import path,include
from . import views


#campo url para cargar la vista de la tienda y hacer el filtrado en la misma
urlpatterns = [
    path('',views.store,name="store"),
    path('category/<slug:category_slug>',views.store, name='product_per_category'),
    path('category/<slug:category_slug>/<slug:product_slug>',views.product_information,name='product_information'),
    path('search/', views.search, name='search')
]