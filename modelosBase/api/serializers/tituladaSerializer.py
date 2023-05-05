from rest_framework import serializers
from modelosBase.models import Titulada

class TituladaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titulada
        fields = '__all__'

        