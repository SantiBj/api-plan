from django.db import models
from usuarioBase.models import Instructor

# Create your models here.

class Programa(models.Model):
    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name = "programa"
        verbose_name_plural = "programas"

    def __str__(self):
        return self.nombre

class Ficha(models.Model):
    numero = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=150)
    programa = models.ForeignKey(Programa,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ficha"
        verbose_name_plural = "fichas"

    def __str__(self):
        return str(self.numero)+" | "+self.nombre

class Competencia(models.Model):
    nombre = models.CharField(max_length=200)
    programa = models.ForeignKey(Programa,on_delete=models.CASCADE) #hace referencia a todos los adsi
    instructores = models.ManyToManyField(Instructor)

    class Meta:
        verbose_name= 'competencia'
        verbose_name_plural= 'competencias'

    def __str__(self):
        return self.nombre
    
class Rap(models.Model):
    nombre = models.CharField(max_length=250)
    competencia = models.ForeignKey(Competencia,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "rap"
        verbose_name_plural = "raps"
    
    def __str__(self):
        return self.nombre
    




