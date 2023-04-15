from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Manager_account(BaseUserManager):
    def create_user(self,name,email,id,phonenumber,addres,password=None):
        
        if not email:
            raise ValueError('El usuario debe registrarse con un correo')
        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            id=id,
            phonenumber = phonenumber,
            addres = addres,
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,name,email,id,phonenumber,addres,password):
        
        user = self.create_user(
            email = self.normalize_email(email),
            name = name,
            id=id,
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
    
    name = models.CharField(max_length=255,null=False,blank=False)
    email = models.EmailField(max_length=200,unique=True,primary_key=True,db_index=True)
    phonenumber = models.CharField(max_length=10,unique=True)#instalar libreria
    addres = models.CharField(max_length=255,null=False)
    id = models.IntegerField(unique=True)
    date = models.DateField(auto_now=False,null=True)
    accept = models.BooleanField(default=False)
    employe_roll = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=5,decimal_places=2,default=15)
    img = models.ImageField(upload_to='profile_img',blank=True)
    
    #atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    
    #roles de django
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','id','phonenumber','addres']
    
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

#por ahora no trabajaremos con el perfil
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=100,blank=True)
    address_2 = models.CharField(max_length=100,blank=True)
    departament = models.CharField(max_length=100,choices=departaments,blank=True)
    city = models.CharField(max_length=100,blank=True)
    zone = models.CharField(max_length=100,blank=True)
    img = models.ImageField(upload_to='profile',blank=True)
    
    def __str__(self):
        return self.user.name
    
    def address(self):
        return f'{self.city} {self.address_1} {self.address_2}'
    
    
    
    