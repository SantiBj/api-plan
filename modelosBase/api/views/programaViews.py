from rest_framework import generics
from modelosBase.api.serializers.programaSerializer import ProgramaSerializer
from modelosBase.models import Programa
from rest_framework.response import Response
from rest_framework import status

# ver programas
class ProgramaListAPIView(generics.ListAPIView):
    serializer_class = ProgramaSerializer

    def get_queryset(self):
        return Programa.objects.all()
    
class ProgramaCreateAPIView(generics.CreateAPIView):
    def post(self, request):
        programa = ProgramaSerializer(data=request.data)
        if programa.is_valid():
            programa.save()
            return Response(programa.data,status=status.HTTP_201_CREATED)
        return Response(programa.errors,status=status.HTTP_406_NOT_ACCEPTABLE)