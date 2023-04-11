from django import forms
from .models import *

class Product_Form(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'