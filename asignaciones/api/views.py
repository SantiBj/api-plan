from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializer import AsignacionesRapSerializer,CrearAsignacionSerializer
from asignaciones.models import AsignacionesRap
from datetime import date,timedelta
from rest_framework import permissions


# crear asignar
# fechas de las asignaciones de una ficha

class CrearAsignacionCreateAPIView(generics.CreateAPIView):

    permission_classes = [permissions.IsAdminUser]
    serializer_class = CrearAsignacionSerializer

    def post(self,request):
        dataSerializer = CrearAsignacionSerializer(data=request.data)

        if dataSerializer.is_valid():
            dataSerializer.save()
            return Response(dataSerializer.data,status=status.HTTP_201_CREATED)
        return Response({"mensaje":"Datos invalidos"},status=status.HTTP_406_NOT_ACCEPTABLE)


class asignacionesInstructorListAPIView(generics.ListAPIView):
    serializer_class = AsignacionesRapSerializer

    def get(self,request,pkInstructor):
        asignacionesInstructor = AsignacionesRap.objects.filter(instructor=pkInstructor)
        # si va vacio se valida para mostrar un error o algo
        asignacionesSerializer = AsignacionesRapSerializer(asignacionesInstructor,many=True)
        return Response(asignacionesSerializer.data,status=status.HTTP_200_OK)

class asignacionesFichaListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AsignacionesRapSerializer

    def get(self,request,pkFicha):
        asignacionesFicha = AsignacionesRap.objects.filter(ficha = pkFicha)
        # si va vacio se valida para mostrar un error o algo
        asignacionesSerializer = AsignacionesRapSerializer(asignacionesFicha,many=True)
        return Response(asignacionesSerializer.data,status=status.HTTP_200_OK)
        

# serializar y sacar las fechas
# en cada onchange del input se valida que no se este intentando asignar en una de estas fechas
@api_view(['GET',])
@permission_classes([IsAdminUser])
def fechasAsignadasFicha(request,pkFicha):
    hoy = date.today()

    #asignaciones futuras
    # ya que el frontend no dejara asignar en una fecha menor a hoy
    rapsAsignados_fechas = AsignacionesRap.objects.filter(
        ficha=pkFicha, fechaFin__gte=hoy
    ).values_list('fechaInicio','fechaFin')

    fechas_ocupadas=[]
    for inicio,fin in rapsAsignados_fechas:
        duracionAsignacion = fin-inicio

        for i in range(duracionAsignacion.days + 1):
            fecha = inicio + timedelta(days=i)
            fechas_ocupadas.append(fecha)

    return Response({
        "fechasOcupadas": fechas_ocupadas
    },status=status.HTTP_200_OK)