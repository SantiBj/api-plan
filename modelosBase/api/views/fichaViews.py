from rest_framework import generics
from modelosBase.api.serializers.fichaSerializer import FichaSerializer,CrearFichaSerializer
from modelosBase.models import Ficha
from rest_framework.response import Response
from rest_framework import status

#crear 
#eliminar
#ver

# fichas pertencientes a un programa
class FichasProgramaListAPIView(generics.ListAPIView):
    queryset = Ficha.objects.all()

    # recibe un id
    def get(self,request, pk):
        print(pk)
        fichas = Ficha.objects.filter(programa = pk).values("numero","nombre") # dicionario con estas keys

        if len(fichas) > 0:
            fichasSerializer = FichaSerializer(fichas,many=True)
            return Response(fichasSerializer.data,status=status.HTTP_200_OK)
        return Response({"mensage":"El programa existe"},status=status.HTTP_404_NOT_FOUND)

class FichaCreateAPIView(generics.CreateAPIView):
    serializer_class = CrearFichaSerializer


    def post(self, request):
        serializer = CrearFichaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"mensaje":"Datos Invalidos"},status=status.HTTP_406_NOT_ACCEPTABLE)

