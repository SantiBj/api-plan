from datetime import timedelta
from django.db.models import Q
from datetime import datetime
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .instructorSerializers import InstructorSerializer, ListaInstructoresSerializer, CrearInstructorSerializer
from usuarioBase.models import Instructor,Sesion
from modelosBase.models import Competencia
from asignaciones.models import AsignacionesRap
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken 
from modelosBase.api.views.Pagination import Pagination

class Inicio_sesion(ObtainAuthToken):
    def post(self,request):
        try:
            documento = int(request.data["username"])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            #si hay token se suma mas uno al registro 
            token = Token.objects.get(user=user)
            sesion = Sesion.objects.get(user=user)
            if (sesion.sesiones == 1):
                return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
            sesion.sesiones = sesion.sesiones+1
            sesion.save()
        except:
            # si no hay token se crea el registro
            sesion = Sesion(user=user)
            sesion.save()
            
        makeToken = Token.objects.get_or_create(user=user)[0]
        return Response({
            "token": str(makeToken),
            "documento": str(user.documento),
            "nombreCompleto": str(user.nombreCompleto),
            "isAdmin": bool(user.is_staff)
        })
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def salir(request):
    # eliminando el token del usuario al salir
    sesion = Sesion.objects.get(user=request.user)

    if(sesion.sesiones == 1):
        sesion.delete()
        Token.objects.get(user=request.user).delete()
    else:
        sesion.sesiones = sesion.sesiones-1
        sesion.save()

    
    return Response(status=status.HTTP_200_OK)

class NombreInstructor(generics.UpdateAPIView):
    permission_classes=[permissions.IsAdminUser]
    serializer_class = CrearInstructorSerializer

    #obtiene instructor a actualizar
    def get_object(self):
        #capturar el id de la url
        user_id = self.kwargs['id']
        return Instructor.objects.get(documento=user_id)

    #recibe los datos a actualizar -> serializer
    #recibe la instancia o objeto obtenido anteriormente
    def perform_update(self, serializer):
        #guarda los cambios
        serializer.save()
        
# buscador instructor por nombre o documento
class BuscadorInstructor(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Instructor.objects.all()
    pagination_class = Pagination

    def get(self, request):
        try:
            busqueda = int(self.request.query_params.get('search', None))
        except:
            busqueda = self.request.query_params.get('search', None)

        instructores = Instructor.objects.filter(
            Q(documento__icontains=busqueda) | Q(nombreCompleto__icontains=busqueda))

        page = self.paginate_queryset(instructores)

        if (instructores):
            serializer = InstructorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response("No hay instructores", status=status.HTTP_404_NOT_FOUND)


# instructor por documento
class InstructoresRetriveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        instructor = Instructor.objects.filter(documento=pk)

        if (instructor):
            serializer = InstructorSerializer(instructor, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class InstructorDestroy(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Instructor.objects.all()


class InstructoresListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    pagination_class = Pagination
    serializer_class = ListaInstructoresSerializer
    queryset = Instructor.objects.all().values("documento", "nombreCompleto")


class CrearInstructorCreateAPIView(generics.CreateAPIView):
    #     {
    #     "documento": 10,
    #     "password": "10",
    #     "is_superuser": true,
    #     "nombreCompleto": "10",
    #     "is_staff": true
    # }
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CrearInstructorSerializer

    def post(self, request):

        serializer = CrearInstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"mensaje": "Datos invalidos"}, status=status.HTTP_406_NOT_ACCEPTABLE)


# devolver instructores disponibles para una fecha y que puedan dictar una competencia


@api_view(['POST',])
@permission_classes([IsAdminUser])
def instructoresDisponiblesFecha(request):
    if request.method == 'POST':
        data = request.data
        '''
        fechaInicial
        idCompetencia
        fechaFin
        '''

        fechaInicioUser = datetime.strptime(
            data['fechaInicial'], '%Y-%m-%d').date()
        idCompetencia = data['idCompetencia']
        fecha_finUser = datetime.strptime(data['fechaFin'], '%Y-%m-%d').date()
        duracionRap = fecha_finUser-fechaInicioUser

        instructoresOcupados = AsignacionesRap.objects.filter(
            fechaInicio__gte=fechaInicioUser,
            fechaFin__lte=fecha_finUser
        ).values_list('instructor')

        id_instructoresOcupados = []

        for instructor in instructoresOcupados:
            id_instructoresOcupados.append(instructor[0])

        instructoresOcupados2 = AsignacionesRap.objects.filter(
            fechaInicio__lte=fecha_finUser,
            fechaFin__gte=fechaInicioUser
        ).values_list('instructor')
        for instructor in instructoresOcupados2:
            id_instructoresOcupados.append(instructor[0])

        allFechasUser = []

        for i in range(duracionRap.days + 1):
            allFechasUser.append(fechaInicioUser+timedelta(days=i))

        for fecha in allFechasUser:
            # instructores que empiezan en una fecha del rango
            instructoresocupados = AsignacionesRap.objects.filter(
                fechaInicio=fecha
            ).values_list('instructor')

            for instructor in instructoresocupados:
                id_instructoresOcupados.append(instructor[0])

            # instructores que finalizan en una fecha del rango
            instructoresop = AsignacionesRap.objects.filter(
                fechaFin=fecha
            ).values_list('instructor')
            for instructor in instructoresop:
                id_instructoresOcupados.append(instructor[0])

        # instructores libres
        instructoresLibres = []

        # trayendo los instructores que pueden dictar la competencia --de la tabla intermedia
        competencia = Competencia.objects.get(pk=idCompetencia)
        instructoresCompetencia = competencia.instructores.all().values('documento',
                                                                        'nombreCompleto')

        for instructor in instructoresCompetencia:
            if not instructor["documento"] in id_instructoresOcupados:
                instructoresLibres.append(instructor)

        Paginacion = Pagination()
        paginacion_data = Paginacion.paginate_queryset(instructoresLibres,request)
        serializer = ListaInstructoresSerializer(paginacion_data, many=True)
        if serializer.data:
            return Paginacion.get_paginated_response(serializer.data)
        return Response([], status=status.HTTP_404_NOT_FOUND)
