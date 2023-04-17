from rest_framework import generics
from modelosBase.api.serializers.fichaSerializer import FichaSerializer, CrearFichaSerializer
from modelosBase.models import Ficha
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db.models import Q
from .Pagination import Pagination

# crear
# eliminar
# ver

# fichas pertencientes a un titulada


class FichaDestroy(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Ficha.objects.all()


class FichaRetrieve(generics.RetrieveAPIView):
    serializer_class = CrearFichaSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, numero):
        ficha = Ficha.objects.filter(numero=numero)
        if (ficha):
            serializer = CrearFichaSerializer(ficha, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("La ficha no existe", status=status.HTTP_404_NOT_FOUND)


class FichaCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CrearFichaSerializer

    def post(self, request):
        serializer = CrearFichaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"mensaje": "Datos Invalidos"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class FichasTituladaListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Ficha.objects.all()
    pagination_class = Pagination

    # recibe un id
    def get(self, request, pk):
        fichas = Ficha.objects.filter(titulada=pk).values(
            "numero", "nombre")  # dicionario con estas keys
        page = self.paginate_queryset(fichas)

        if (fichas):
            fichasSerializer = FichaSerializer(page, many=True)
            return self.get_paginated_response(fichasSerializer.data)
        return Response("la titulada no tiene fichas", status=status.HTTP_404_NOT_FOUND)


class FichaTituladaBuscador(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Ficha.objects.all()
    pagination_class = Pagination

    def get(self, request):
        busqueda = int(self.request.query_params.get('search', None))
        titulada = int(self.request.query_params.get('programa', None))

        consulta = Ficha.objects.filter(
            Q(numero__icontains=busqueda) & Q(titulada=titulada))

        page = self.paginate_queryset(consulta)
        if (consulta):
            serializer = CrearFichaSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response("no hay fichas", status=status.HTTP_404_NOT_FOUND)


class FichaBuscador(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Ficha.objects.all()
    pagination_class = Pagination

    def get(self, request):
        busqueda = int(self.request.query_params.get('search', None))
        fichas = Ficha.objects.filter(numero__icontains=busqueda)

        # paginar la consulta osea dividir la respuesta en paginas
        page = self.paginate_queryset(fichas)
        if (fichas):
            # serializar(pasar objeto a json) los datos de la pagina
            serializer = CrearFichaSerializer(page, many=True)
            # si hay datos se responde con get_paginated para tener la info de numero paginas,etc..
            return self.get_paginated_response(serializer.data)
        return Response("No hay fichas", status=status.HTTP_404_NOT_FOUND)


class FichasListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Ficha.objects.all()
    serializer_class = CrearFichaSerializer
    pagination_class = Pagination
