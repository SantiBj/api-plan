from rest_framework import generics
from modelosBase.models import Competencia
from modelosBase.api.serializers.competenciasSerializer import CompetenciasSerializers
from rest_framework.response import Response
from rest_framework import status
# ver competencias por ficha que pertenece a un programa


class CompetenciasProgramaListAPIView(generics.ListAPIView):

    def get(self,request, pkPrograma):

        competencias = Competencia.objects.filter(programa=pkPrograma)

        if len(competencias) > 0:
            competenciasSerializer = CompetenciasSerializers(competencias,many=True)
            return Response(competenciasSerializer.data,status=status.HTTP_200_OK)
        return Response({"mensaje":"No hay competencias para este programa"},status=status.HTTP_404_NOT_FOUND)
    

        