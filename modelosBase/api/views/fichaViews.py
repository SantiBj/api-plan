from rest_framework import generics
from modelosBase.api.serializers.fichaSerializer import FichaSerializer,CrearFichaSerializer
from modelosBase.models import Ficha
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db.models import Q

#crear 
#eliminar
#ver

# fichas pertencientes a un programa
class FichasProgramaListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Ficha.objects.all()

    # recibe un id
    def get(self,request, pk):
        fichas = Ficha.objects.filter(programa = pk).values("numero","nombre") # dicionario con estas keys

        if len(fichas) > 0:
            fichasSerializer = FichaSerializer(fichas,many=True)
            return Response(fichasSerializer.data,status=status.HTTP_200_OK)
        return Response({"mensage":"El programa existe"},status=status.HTTP_404_NOT_FOUND)

class FichaCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CrearFichaSerializer


    def post(self, request):
        serializer = CrearFichaSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"mensaje":"Datos Invalidos"},status=status.HTTP_406_NOT_ACCEPTABLE)

class FichaProgramaBuscador(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Ficha.objects.all()

    def get(self,request):
        busqueda = int(self.request.query_params.get('search',None))
        programa = int(self.request.query_params.get('programa',None))

        print(busqueda)

        if busqueda:
            consulta = Ficha.objects.filter(Q(numero__icontains=busqueda) & Q(programa=programa) )
            serializer = CrearFichaSerializer(consulta,many=True)
            if (serializer.data):
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response("no hay fichas",status=status.HTTP_404_NOT_FOUND)
        return Response("no hay fichas",status=status.HTTP_404_NOT_FOUND)
