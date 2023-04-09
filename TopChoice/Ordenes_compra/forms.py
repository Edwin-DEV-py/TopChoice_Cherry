from django import forms
from .models import Order

class Orden_Form(forms.ModelForm):
    class Meta:
        model=Order
        fields = ['user_name','email','phonenumber','address_1','address_2','city','departament','country','order_note']