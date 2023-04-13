from django.urls import path
from . import views

urlpatterns = [
    path('order/',views.order,name='order'),
    path('payment/',views.payment,name='payment'),
    path('complete/',views.complete,name='complete'),
]