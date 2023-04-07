from django.shortcuts import render
from .forms import *

# Create your views here.


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid(): #aqui verificamos los datos del ciente y los guardamos
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            id = form.cleaned_data['id']
            addres = form.cleaned_data['addres']
            phonenumber = form.cleaned_data['phonenumber']
            date = form.cleaned_data['date']
            password = form.cleaned_data['password']
            user = User.objects.create_user(name=name,email=email,id=id,addres=addres,phonenumber=phonenumber,password=password)
            user.date = date
            user.save()
    
    context = {
        'form':form
    }
    return render(request,'user/registro.html',context)