from datetime import timedelta
from datetime import datetime
from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .instructorSerializers import ListaInstructoresSerializer,CrearInstructorSerializer
from usuarioBase.models import Instructor
from modelosBase.models import Competencia
from asignaciones.models import AsignacionesRap

# instructores disponibles en una fecha

class InstructoresListAPIView(generics.ListAPIView):
    serializer_class = ListaInstructoresSerializer

    #consulta
    # solo self 
    # metodos como get patch put post delete si requeiren el request
    def get_queryset(self):
        return Instructor.objects.all().values("documento","nombreCompleto")


class CrearInstructorCreateAPIView(generics.CreateAPIView):
    serializer_class = CrearInstructorSerializer


    def post(self,request):
        
        serializer = CrearInstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"mensaje":"Datos invalidos"},status=status.HTTP_406_NOT_ACCEPTABLE)
    

# devolver instructores disponibles para una fehca y que puedan dictar una competencia
@api_view(['POST',])
def instructoresDisponiblesFecha(request):
    if request.method == 'POST':

        data = request.data

        fechaInicioUser = datetime.strptime(
            data['fechaInicial'], '%Y-%m-%d').date()
        idCompetencia = data['idCompetencia']
        fecha_finUser = datetime.strptime(data['fechaFin'], '%Y-%m-%d').date()
        duracionRap = fecha_finUser-fechaInicioUser

        #333333333333333333333333333333333333333333333

        instructoresOcupados = AsignacionesRap.objects.filter(
            fechaInicio__gte = fechaInicioUser,
            fechaFin__lte = fecha_finUser
        ).values_list('instructor')

        id_instructoresOcupados = []

        for instructor in instructoresOcupados:
            id_instructoresOcupados.append(instructor[0])

        instructoresOcupados2 = AsignacionesRap.objects.filter(
            fechaInicio__lte = fecha_finUser,
            fechaFin__gte = fechaInicioUser
        ).values_list('instructor')
        for instructor in instructoresOcupados2:
            id_instructoresOcupados.append(instructor[0])

        allFechasUser = []

        for i in range(duracionRap.days + 1):
            allFechasUser.append(fechaInicioUser+timedelta(days=i))

        for fecha in allFechasUser:
            # instructores que empiezan en una fecha del rango
            instructoresocupados = AsignacionesRap.objects.filter(
                fechaInicio = fecha
            ).values_list('instructor')

            for instructor in instructoresocupados:
                id_instructoresOcupados.append(instructor[0])
            
            # instructores que finalizan en una fecha del rango
            instructoresop = AsignacionesRap.objects.filter(
                fechaFin = fecha
            ).values_list('instructor')
            for instructor in instructoresop:
                id_instructoresOcupados.append(instructor[0])

        #instructores libres
        instructoresLibres = []

        competencia = Competencia.objects.get(pk=idCompetencia)
        instructoresCompetencia = competencia.instructores.all().values('documento','nombreCompleto')

        for instructor in instructoresCompetencia:
            if not instructor["documento"] in id_instructoresOcupados:
                instructoresLibres.append(instructor)
            
        serializer = ListaInstructoresSerializer(instructoresLibres,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
