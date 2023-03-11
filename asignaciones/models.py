from django.db import models
from modelosBase.models import *
from usuarioBase.models import Instructor

# Create your models here.

class AsignacionesRap(models.Model):
    ficha = models.ForeignKey(Ficha,on_delete=models.CASCADE)
    rap = models.ForeignKey(Rap,on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    

    class Meta:
        verbose_name= "asignacion"
        verbose_name_plural = "asignaciones"

    def __str__(self):
        return self.ficha.numero+" | " + self.instructor.nombre