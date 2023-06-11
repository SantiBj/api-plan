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
from .tokenPDF import user,password



# informes

class ReportFicha(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
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

        client = pdfcrowd.HtmlToPdfClient(user,password)
        pdf_file = client.convertString(html)
        
        response = HttpResponse(pdf_file,content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe.pdf"'
        return response

class Report(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
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

        client = pdfcrowd.HtmlToPdfClient(user,password)
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
        
#lista de asignaciones cuya fecha de finalizacion sea mayor a hoy
#ficha
class AsignacionesActivasFichas(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AsignacionesRapSerializer

    def get(self, request, *args, **kwargs):
        hoy = date.today()
        asignaciones = AsignacionesRap.objects.filter(Q(ficha=self.kwargs["ficha"])&Q(fechaFin__gte=hoy)).order_by("fechaInicio")
        serializer = AsignacionesRapSerializer(asignaciones,many=True)
        if len(serializer.data) > 0:
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
#instructor

class AsignacionesActivasInstructor(generics.ListAPIView):
    permission_classes=[permissions.AllowAny]
    serializer_class = AsignacionesRapSerializer

    def get(self, request, *args, **kwargs):
        hoy = date.today()
        asignaciones = AsignacionesRap.objects.filter(Q(instructor=self.kwargs["doc"])
                                                      &Q(fechaFin__gte=hoy))
        serializer = AsignacionesRapSerializer(asignaciones,many=True)
        if len(serializer.data) > 0:
            return Response(serializer.data,status=status.HTTP_200_OK) 
        return Response(status=status.HTTP_404_NOT_FOUND)

#eliminar asignacion por <int:id> 
class DeleteAsignacion(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = AsignacionesRap.objects.all()


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