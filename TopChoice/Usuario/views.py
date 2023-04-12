from django.shortcuts import render,redirect
from .forms import *
from Carrito.views import _cart_id
from Carrito.models import *
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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

#funcion para iniciar sesion
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email,password=password) #metodo de autenticacion
        
        if user is not None:
            
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                items_in_cart = Cart_item.objects.filter(cart=cart).exists()
                if items_in_cart:
                    items = Cart_item.objects.filter(cart=cart)
                    for item in items:
                        item.user = user 
                        item.save()
            except:
                pass
            
            auth.login(request, user)
            return redirect('header')
        
        else:
            messages.error(request, 'Usuario invalido')
    return render(request,'index.html')

#funcion para cerrar sesion
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Saliste exitosamente')
    
    return redirect('header')

#funcion para crear la vista del perfil
@login_required(login_url='login')
def profile(request):
    return render(request,'user/perfil.html')

@login_required(login_url='login')
def edit_profile(request,id):
    perfil= User.objects.get(id=id)
    if request.method == 'GET':
        form = EditForm(instance=perfil)
        contesto = {'form':form,'perfil':perfil}
    else:
        form = EditForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'user/editar_perfil.html', contesto)

#funcion para el envio del correo para recuperar contrasena
def forgot(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        #validamos que el usuario exista
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            #parametros del correo que leera el usuario
            page = get_current_site(request)
            mail = 'Restaura tu contrasena'
            body = render_to_string('user/restaurar.html',{
                'user':user,
                'domain':page,
                'user_id':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            user_email = email
            send_mail = EmailMessage(
                mail,body,settings.EMAIL_HOST_USER,to=[user_email]
            )
            send_mail.from_email = False
            send_mail.send()
            
            messages.success(request,'Revisa tu correo para restaurar tu contrasena')
            return redirect('forgot')
        
        else:
            messages.error(request,'La cuenta no existe')
            return redirect('forgot')
            
    return render(request,'user/forgot.html')

#funcion para validar al usuario
def validation_user(request,uidb64,token):
    #obtenemo el id
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=user_id)
    except(TypeError,ValueError,OverflowError, User.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['user_id']=user_id
        messages.success(request,'Restaura tu contrasena')
        return redirect('restart_password')
    else:
        messages.error(request,'Link no valido')
        return redirect('header')
    
#funcion que crea la vista para reiniciar contrasena
def restart_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        #validamos que la contrasenas coincidan
        if password == confirm_password:
            user_id = request.session.get('user_id')
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Contrasena actualizada')
            return redirect('header')
        else:
            messages.error(request, 'Contrasenas no coinciden')
            return redirect('restart')
        
    else:
        return render(request,'user/reiniciar.html')
    
    
#lista de usuario para compartir
@login_required
@user_passes_test(lambda user: user.employe_roll or user.is_admin,login_url='login')
def inventary_user(request):
    users = User.objects.all()
    pagination = Paginator(users,40)
    page = request.GET.get('page',1)
    page_x_user = pagination.get_page(page)
    num_pages = pagination.num_pages
    start = max(1, int(page)-2)
    end = min(num_pages,int(page)+2)
    if start == 1:
        end = min(5, num_pages)
    elif end == num_pages:
        start = max(num_pages - 4,1)
    page_range = range(start,end+1)
    context = {'users':page_x_user,'page_range':page_range}
    return render(request,'administracion/inventario_user.html',context)