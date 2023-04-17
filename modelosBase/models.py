from django.db import models
from usuarioBase.models import Instructor

# Create your models here.


class Competencia(models.Model):
    nombre = models.CharField(max_length=200)
    instructores = models.ManyToManyField(Instructor)

    class Meta:
        verbose_name = 'competencia'
        verbose_name_plural = 'competencias'

    def __str__(self):
        return self.nombre


class Titulada(models.Model):
    nombre = models.CharField(max_length=200)
    competencias = models.ManyToManyField(Competencia)

    class Meta:
        verbose_name = "titulada"
        verbose_name_plural = "tituladas"

    def __str__(self):
        return self.nombre


class Ficha(models.Model):
    numero = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=150)
    titulada = models.ForeignKey(Titulada, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ficha"
        verbose_name_plural = "fichas"

    def __str__(self):
        return str(self.numero)+" | "+self.nombre


class Rap(models.Model):
    nombre = models.CharField(max_length=250)
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "rap"
        verbose_name_plural = "raps"

    def __str__(self):
        return self.nombre
