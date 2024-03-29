from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..serializers.rapSerializers import RapNoAsignadosSerializer
from modelosBase.models import Rap
from asignaciones.models import AsignacionesRap
from rest_framework import permissions



# raps sin asignar por ficha
class RapSinAsignarDeCompetenciaListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = RapNoAsignadosSerializer
    queryset = Rap.objects.all()


    def get(self, request , pkCompetencia,numeroficha):
        #traer los rap de la competencia
        rapsCompetencia = Rap.objects.filter(competencia = pkCompetencia)

        # values trae los datos en un array de diccionarios ya no querysets o objetos
        # traer todas los raps asignados a la ficha en un array
        # values List trae solo los valores de una lista de tuplas[(1,),(2,)] y en flat = True una lista plana [1,2]
        rapsAsignados = AsignacionesRap.objects.filter(ficha = numeroficha).values_list("rap",flat=True) 

        # mirar cuales de los rap no han sido asignados y devolverlos en una array de objetos
        rapsSinAsignar = []
        
        for rap in rapsCompetencia:
            if not rap.pk in rapsAsignados:
                rapsSinAsignar.append(rap)


        if rapsSinAsignar:
            #devolviendo los raps sin asignar de la competencia pedida
            serializer = RapNoAsignadosSerializer(rapsSinAsignar,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response([],status=status.HTTP_404_NOT_FOUND)

        

        

