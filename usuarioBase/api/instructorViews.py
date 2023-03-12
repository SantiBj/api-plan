from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .instructorSerializers import ListaInstructoresSerializer,CrearInstructorSerializer
from usuarioBase.models import Instructor
# instructores disponibles en una fecha

class InstructoresListAPIView(generics.ListAPIView):
    serializer_class = ListaInstructoresSerializer

    #consulta
    # solo self 
    # metodos como get patch put post delete si requeiren el request
    def get_queryset(self):
        return Instructor.objects.all().values("documento","nombreCompleto")


class CrearInstructorCreateAPIView(generics.CreateAPIView):
    serializer_class = CrearInstructorSerializer


    def post(self,request):
        
        serializer = CrearInstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({"mensaje":"Datos invalidos"},status=status.HTTP_406_NOT_ACCEPTABLE)
