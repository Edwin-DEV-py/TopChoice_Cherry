from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages

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
            
            messages.success(request, 'Usuario registrado correctamente')
            return redirect('header')
    
    context = {
        'form':form
    }
    return render(request,'user/registro.html',context)