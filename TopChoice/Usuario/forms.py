from django import forms
from .models import User

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
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Contrasena',
        'class':'form-control bg-transparent border-0',
        'type':'password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirmar contrasena',
        'class':'form-control bg-transparent border-0',
        'type':'password'
    }))
    class Meta:
        model = User
        fields = ['name','email','id','phonenumber','addres','date','password']