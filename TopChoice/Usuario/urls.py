from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('forgot/',views.forgot,name='forgot'),
    path('restart_password/',views.restart_password,name='restart_password'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('validation_user/<uidb64>/<token>/',views.validation_user,name='validation_user'),
    path('inventario_user.html',views.inventary_user,name='inventary_user'),
    path('edit_profile/<int:id>/',views.edit_profile,name='edit_profile'),
    path('excel/', views.excel, name='excel'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('change_password/',views.change_password,name='change_password')
]