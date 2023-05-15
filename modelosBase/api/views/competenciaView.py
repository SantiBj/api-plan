from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser,AllowAny
from modelosBase.models import Competencia, Titulada
from usuarioBase.models import Instructor
from modelosBase.api.serializers.competenciasSerializer import CompetenciasSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .Pagination import Pagination

# datos de una competencia


class CompetenciaRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CompetenciasSerializers

    def get(self, request, pk):
        competencia = Competencia.objects.get(pk=int(pk))

        if competencia:
            serializer = CompetenciasSerializers(competencia)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("la competencia no existe", status=status.HTTP_404_NOT_FOUND)

# buscador competencia


class BuscadorCompetencias(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Competencia.objects.all()
    pagination_class = Pagination

    def get(self, request):
        busqueda = self.request.query_params.get('search', None)
        consulta = Competencia.objects.filter(nombre__icontains=busqueda)

        page = self.paginate_queryset(consulta)

        if (consulta):
            serializer = CompetenciasSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response("no hay competencias", status=status.HTTP_404_NOT_FOUND)


class CompetenciasList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Competencia.objects.all()
    serializer_class = CompetenciasSerializers
    pagination_class = Pagination


class CompetenciasTituladaListAPIView(generics.ListAPIView):

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        # consultando las competencias que pertenecen a la titulada en la tabla intermedia
        titulada = Titulada.objects.get(pk=pk)
        competencias = titulada.competencias.all().values("pk", "nombre")
        # values -> [{"pk":1,"nombre":"algo"}] diccionario con estas keys
        # values_list -> solo el valor en un array de tuplas [(1,),(2,)]
        # values_list, flat = True -> valores en un array [1,2]

        if len(competencias) > 0:
            competenciasSerializer = CompetenciasSerializers(
                competencias, many=True)
            return Response(competenciasSerializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_404_NOT_FOUND)


# añadir un instructor a una competencia
#################################################corregir los permisos para que no cualquiera pueda acceder
@api_view(["POST",])
@permission_classes([AllowAny])
def anadirInstructorACompetencia(request):
    if request.method == 'POST':
        print(request.data)
        competencia = Competencia.objects.get(pk=int(request.data["pkCompetencia"]))
        instructor = Instructor.objects.get(
            documento=int(request.data["docInstructor"]))
        try:
            competencia.instructores.add(instructor)
            competencia.save()
            return Response({"mensaje": "se añadio con exito el instructor a la competencia"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"mensaje": "Error al añadir el instructor a la competencia", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CompetenciasInstructorList(generics.ListAPIView):

    permission_classes=[permissions.AllowAny]

    def get(self, request,documento):  
        #consultar el instructor y luego sus competencias
        instructor = Instructor.objects.get(documento = documento)

        competencias = instructor.competencia_set.all()

        if (len(competencias)>0):
            serializer = CompetenciasSerializers(competencias,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response([],status=status.HTTP_404_NOT_FOUND)
    
class DeleteCompetenciaInstructor(generics.DestroyAPIView):

    permission_classes = [permissions.AllowAny]

    def delete(self,request,documento,pk):
        try:
            instructor = Instructor.objects.get(documento=documento)
            #obteniendo el registro de la tabla intermedia
            # obteniendo la relacion entre el instructor y la competencia para eliminar este registro
            #en get se pasa el id de la competencia a trae
            competencia = instructor.competencia_set.get(id = pk)
            #eliminando el registro o relacion a la tabla intermedia
            instructor.competencia_set.remove(competencia)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        