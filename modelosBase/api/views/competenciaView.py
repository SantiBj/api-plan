from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from modelosBase.models import Competencia, Titulada
from usuarioBase.models import Instructor
from modelosBase.api.serializers.competenciasSerializer import CompetenciasSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .Pagination import Pagination

#buscador competencia
class BuscadorCompetencias(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Competencia.objects.all()
    pagination_class= Pagination

    def get(self,request):
        busqueda = self.request.query_params.get('search',None)
        consulta = Competencia.objects.filter(nombre__icontains=busqueda)

        page= self.paginate_queryset(consulta)

        if(consulta):
            serializer = CompetenciasSerializers(page,many=True)
            return self.get_paginated_response(serializer.data)
        return Response("no hay competencias", status=status.HTTP_404_NOT_FOUND)

class CompetenciasList(generics.ListAPIView):
    permission_classes=[permissions.IsAdminUser]
    queryset=Competencia.objects.all()
    serializer_class=CompetenciasSerializers
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
@api_view(["POST",])
@permission_classes([IsAdminUser])
def anadirInstructorACompetencia(request):
    if request.method == 'POST':
        competencia = Competencia.objects.get(pk=request.data["pkCompetencia"])
        instructor = Instructor.objects.get(
            documento=request.data["docInstructor"])
        try:
            competencia.instructores.add(instructor)
            competencia.save()
            return Response({"mensaje": "se añadio con exito el instructor a la competencia"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"mensaje": "Error al añadir el instructor a la competencia", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
