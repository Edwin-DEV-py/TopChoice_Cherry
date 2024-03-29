"""TopChoice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.header, name="header"),
    path('store/',include('Productos.urls')),
    path('shopping_cart/',include('Carrito.urls')),
    path('user/',include('Usuario.urls')),
    path('orders/',include('Ordenes_compra.urls')),
    path('terms_conditions',views.terms_conditions,name='terms_conditions')
    #aqui colocar la etiqueta include para usar las urls de las otras apps.
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

