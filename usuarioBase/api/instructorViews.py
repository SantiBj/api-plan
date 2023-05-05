from datetime import timedelta
from django.db.models import Q
from datetime import datetime
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .instructorSerializers import InstructorSerializer, ListaInstructoresSerializer, CrearInstructorSerializer
from usuarioBase.models import Instructor
from modelosBase.models import Competencia
from asignaciones.models import AsignacionesRap
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from modelosBase.api.views.Pagination import Pagination

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
    permission_classes = [permissions.IsAdminUser]

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


@api_view(['DELETE'])
def salir(request):
    # eliminando el token del usuario al salir
    Token.objects.get(user=request.user).delete()
    return Response(status=status.HTTP_200_OK)

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

        serializer = ListaInstructoresSerializer(instructoresLibres, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_404_NOT_FOUND)
