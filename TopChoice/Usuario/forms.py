from django import forms
from .models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Nombre',
        'class':'form-control bg-transparent border-0',
        'type':'text'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder':'Email',
        'class':'form-control bg-transparent border-0',
        'type':'email'
    }))
    id = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder':'Identificacion',
        'class':'form-control bg-transparent border-0',
        'type':'number'
    }))
    addres = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Direccion',
        'class':'form-control bg-transparent border-0',
        'type':'text'
    }))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Telefono',
        'class':'form-control bg-transparent border-0',
        'type':'text'
    }))
    date = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Fecha',
        'class':'form-control bg-transparent border-0',
        'type':'date'
    }))
    accept = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class':'check',
        'id':'chec'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Contraseña',
        'class':'form-control bg-transparent border-0',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirmar contraseña',
        'class':'form-control bg-transparent border-0',
    }))
    class Meta:
        model = User
        fields = ['name','email','id','phonenumber','addres','date','password','accept']
        
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean() #accedemos a los datos del form
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data
    
class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','email','phonenumber','addres','id','img']