from rest_framework import generics
from modelosBase.api.serializers.fichaSerializer import FichaProgramaSerializer
from modelosBase.models import Ficha
from rest_framework.response import Response
from rest_framework import status

#crear 
#eliminar
#ver

# fichas pertencientes a un programa
class FichasPrograma(generics.ListAPIView):
    # recibe un id
    def get(self, request, pk , *args, **kwargs):
        try:
            fichas = Ficha.objects.filter(programa = pk).values("numero","nombre")
            fichasSerializer = FichaProgramaSerializer(fichas)
            return Response(fichasSerializer.data,status=status.HTTP_200_OK)
        except:
            return Response({"mensage":"El programa existe"},status=status.HTTP_404_NOT_FOUND)


