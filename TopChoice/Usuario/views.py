from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

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
            
            #verificamos el email
            page = get_current_site(request)
            mail = 'Activa tu cuenta para continuar'
            body = render_to_string('user/verificacion.html',{
                'user':user,
                'domain':page,
                'user_id': urlsafe_base64_encode( force_bytes(user.pk)), #obtenemos el id del usuario pero la trasnportamos codificada en hexadecimal para no vulnerar la informacion
                'token':default_token_generator.make_token(user)
            })
            user_email = email
            send_mail = EmailMessage(
                mail,body,settings.EMAIL_HOST_USER,to=[user_email]
            )
            send_mail.from_email = False
            send_mail.send()
            
            #mandamos mensaje de autenticacion
            #messages.success(request, 'Usuario registrado correctamente')
            return redirect('/user/register/?command=verification&email='+email)
    
    context = {
        'form':form
    }
    return render(request,'user/registro.html',context)

#funcion para activar tu cuenta
def activate(request,uidb64,token):
    try:
        user_id=urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=user_id)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        user = None
        
    #cuando el usuario verifica el correo qued activo en el sistema
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Cuenta activada correctamente')
        return redirect('header')
    
    else:
        messages.error(request,'No se pudo activar tu cuenta')
        return redirect('register')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email,password=password)
        
        if user is not None:
            auth.login(request, user)
            
            return redirect('header')
        
        else:
            messages.error(request, 'Usuario invalido')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Saliste exitosamente')
    
    return redirect('header')