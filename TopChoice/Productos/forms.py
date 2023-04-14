from django import forms
from .models import *

class Product_Form(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['price','stock','is_available']
        
        
class Comment_Form(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['title','comment','rating']