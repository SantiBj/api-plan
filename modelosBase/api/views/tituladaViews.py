from rest_framework import generics
from modelosBase.api.serializers.tituladaSerializer import TituladaSerializer
from modelosBase.models import Titulada
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


# ver tituladas
class TituladaListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = TituladaSerializer

    def get_queryset(self):
        return Titulada.objects.all()

