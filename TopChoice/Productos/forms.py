from django import forms
from .models import *

class Product_Form(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name','price','stock','is_available']