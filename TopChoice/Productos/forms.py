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
        
class filter(forms.Form):
    order_by = forms.ChoiceField(label='Ordenar por',choices=(
        ('asc','Productos de la A-Z'),
        ('desc','Productos de la Z-A'),
        ('min','Precio Menor a Mayor'),
        ('max','Precio Mayor a Menor'),
    ),required=False)