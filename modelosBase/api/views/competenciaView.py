from rest_framework import generics
from rest_framework.decorators import api_view
from modelosBase.models import Competencia
from usuarioBase.models import Instructor
from modelosBase.api.serializers.competenciasSerializer import CompetenciasSerializers
from rest_framework.response import Response
from rest_framework import status
# ver competencias por ficha que pertenece a un programa

# sirve pasar todos los campos para ver los instructores asignados
class CompetenciasProgramaListAPIView(generics.ListAPIView):

    def get(self,request, pkPrograma):

        # va pk cuando el id lo genera django
        competencias = Competencia.objects.filter(programa=pkPrograma).values("pk","nombre")
        # values -> {"pk":1,"nombre":"algo"} diccionario con estas keys
        # values_list -> solo el valor en un array de tuplas [(1,),(2,)]
        # values_list, flat = True -> valores en un array [1,2]

        if len(competencias) > 0:
            competenciasSerializer = CompetenciasSerializers(competencias,many=True)
            return Response(competenciasSerializer.data,status=status.HTTP_200_OK)
        return Response({"mensaje":"No hay competencias para este programa"},status=status.HTTP_404_NOT_FOUND)
    
#añadir un instructor a una competencia
@api_view(["POST",])
def anadirInstructorACompetencia(request):
    if request.method == 'POST':
        competencia = Competencia.objects.get(pk = request.data["pkCompetencia"])
        instructor = Instructor.objects.get(documento=request.data["docInstructor"])
        try:
            competencia.instructores.add(instructor)
            return Response({"mensaje":"se añadio con exito el instructor a la competencia"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"mensaje":"Error al añadir el instructor a la competencia", "error": str(e)},status=status.HTTP_400_BAD_REQUEST)
                
            