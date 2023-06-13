from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Editando el manager por defecto de usuario para poder crearlo con los campos deseados
class InstructorManager(BaseUserManager):
    def _create_user(self,documento,nombreCompleto,password,is_staff,is_superuser,**extra_fields):
        instructor = self.model(
            documento = documento,
            nombreCompleto = nombreCompleto,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        instructor.set_password(password)
        instructor.save()
        return instructor

    def create_user(self,documento,nombreCompleto,password = None,**extra_fields):
        return self._create_user(documento,nombreCompleto,password,False,False,**extra_fields)

    def create_superuser(self,documento,nombreCompleto,password = None,**extra_fields):
        return self._create_user(documento,nombreCompleto,password,True,True,**extra_fields)

# Editando el usuario por defecto
class Instructor(AbstractBaseUser, PermissionsMixin):
    documento = models.IntegerField(primary_key=True)
    nombreCompleto = models.CharField(max_length=150)
    objects = InstructorManager()

    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default= False)
    USERNAME_FIELD = 'documento' #indica que al inciar sesion validara este como si fuera el correo o username
    REQUIRED_FIELDS = ['nombreCompleto',]

    class Meta:
        verbose_name = "instructor"
        verbose_name_plural = "instructores"

    def __str__(self):
        return self.nombreCompleto
    
class Sesion(models.Model):
    user = models.OneToOneField(Instructor,unique=True,on_delete=models.CASCADE,verbose_name="user_id")
    sesiones = models.IntegerField(verbose_name="cant_sesiones",default=1) 

    class Meta:
        verbose_name="sesion"
        verbose_name_plural="sesiones"