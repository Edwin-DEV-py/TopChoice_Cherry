from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Manager_account(BaseUserManager):
    def create_user(self,first_name,fisrt_last_name,second_last_name,email,phonenumber,addres,password=None):
        
        if not email:
            raise ValueError('El usuario debe registrarse con un correo')
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            fisrt_last_name = fisrt_last_name,
            second_last_name = second_last_name,
            phonenumber = phonenumber,
            addres = addres,
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,first_name,fisrt_last_name,second_last_name,email,phonenumber,addres,password):
        
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            fisrt_last_name = fisrt_last_name,
            second_last_name = second_last_name,
            phonenumber = phonenumber,
            addres = addres,
        )
        
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
        
class User(AbstractBaseUser):
    
    first_name = models.CharField(max_length=30,null=False,blank=False)
    second_name = models.CharField(max_length=30,null=True)
    fisrt_last_name = models.CharField(max_length=30,null=False,blank=False)
    second_last_name = models.CharField(max_length=30,null=False,blank=False)
    email = models.EmailField(max_length=200,unique=True,primary_key=True)
    phonenumber = models.CharField(max_length=10,unique=True)#instalar libreria
    addres = models.CharField(max_length=200,null=False)
    date = models.DateField(auto_now=False,null=True)
    accept = models.BooleanField(default=False)
    employe_roll = models.BooleanField(default=False)
    
    #atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    
    #roles de django
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','fisrt_last_name','second_last_name','phonenumber','addres']
    
    objects = Manager_account() #instanciamos la clase
    
    #valores a pintar al listar los usuarios
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True

departaments = [
    
]   

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=100,blank=True)
    address_2 = models.CharField(max_length=100,blank=True)
    departament = models.CharField(max_length=100,choices=departaments,blank=True)
    city = models.CharField(max_length=100,blank=True)
    zone = models.CharField(max_length=100,blank=True)
    
    def __str__(self):
        return self.user.first_name
    
    def address(self):
        return f'{self.city} {self.address_1} {self.address_2}'
    
    
    
    