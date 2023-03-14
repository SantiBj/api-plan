from rest_framework import serializers
from asignaciones.models import AsignacionesRap
from usuarioBase.api.instructorSerializers import ListaInstructoresSerializer
from modelosBase.api.serializers.fichaSerializer import FichaSerializer
from modelosBase.api.serializers.rapSerializers import RapNoAsignadosSerializer

class AsignacionesRapSerializer(serializers.ModelSerializer):

    # para ver los datos de las relaciones y no solo el id de estas
    ficha = FichaSerializer()
    rap = RapNoAsignadosSerializer()
    instructor = ListaInstructoresSerializer()

    class Meta:
        model = AsignacionesRap
        fields = '__all__'


class CrearAsignacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionesRap
        fields = '__all__'

