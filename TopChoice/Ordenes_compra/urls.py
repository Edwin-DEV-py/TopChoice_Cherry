from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('order/',views.order,name='order'),
    path('payment/',views.payment,name='payment'),
    path('complete/',views.complete,name='complete'),
    path('order/<int:order_note>/',views.order_detail,name='order_detail')
]