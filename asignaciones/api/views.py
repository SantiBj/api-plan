from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializer import AsignacionesRapSerializer,CrearAsignacionSerializer
from asignaciones.models import AsignacionesRap
from datetime import date,timedelta,datetime
from rest_framework import permissions
from django.http import HttpResponse
import pdfcrowd
from django.shortcuts import render
from usuarioBase.models import Instructor
from modelosBase.models import Ficha
from django.db.models import Q




# informes

class ReportFicha(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = AsignacionesRap.objects.all()
    serializer_class = AsignacionesRap

    def get(self, request):
        NFicha = int(self.request.query_params.get('id',None))
        fechaInicio = datetime.strptime(self.request.query_params.get('inicio',None),'%Y-%m-%d').date()
        fechaFin = datetime.strptime(self.request.query_params.get('fin',None),'%Y-%m-%d').date()


        ficha = Ficha.objects.get(numero = NFicha)
        asignaciones = AsignacionesRap.objects.filter(Q(ficha = ficha)
                                                      &Q(fechaInicio__gte=fechaInicio)
                                                      &Q(fechaFin__lte=fechaFin) )



        context = {
            "fechaInicio":fechaInicio,
            "fechaFin":fechaFin,
            "ficha":ficha,
            "asignaciones":asignaciones,
        }

        #obteniendo el html con .content
        html = render(request,"index.html",context).content

        client = pdfcrowd.HtmlToPdfClient('plan','a1172f72a7e1220d462b5a6293422d41')
        pdf_file = client.convertString(html)
        
        response = HttpResponse(pdf_file,content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe.pdf"'
        return response

class Report(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = AsignacionesRap.objects.all()
    serializer_class = AsignacionesRap

    def get(self, request):
        idInstructor = int(self.request.query_params.get('id',None))
        fechaInicio = datetime.strptime(self.request.query_params.get('inicio',None),'%Y-%m-%d').date()
        fechaFin = datetime.strptime(self.request.query_params.get('fin',None),'%Y-%m-%d').date()


        instructor = Instructor.objects.get(documento = idInstructor)
        asignaciones = AsignacionesRap.objects.filter(Q(instructor = instructor)
                                                      &Q(fechaInicio__gte=fechaInicio)
                                                      &Q(fechaFin__lte=fechaFin) )


        context = {
            "fechaInicio":fechaInicio,
            "fechaFin":fechaFin,
            "instructor":instructor,
            "asignaciones":asignaciones,
        }

        html = render(request,"index.html",context).content

        client = pdfcrowd.HtmlToPdfClient('plan','a1172f72a7e1220d462b5a6293422d41')
        pdf_file = client.convertString(html)
        
        response = HttpResponse(pdf_file,content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe.pdf"'
        return response

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