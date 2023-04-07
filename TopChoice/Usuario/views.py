from django.shortcuts import render
from .forms import *

# Create your views here.


def register(request):
    form = RegisterForm()
    context = {
        'form':form
    }
    return render(request,'user/registro.html',context)