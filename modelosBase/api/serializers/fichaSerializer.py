from rest_framework import serializers
from modelosBase.models import Ficha

# fichas pertencientes a un programa

class FichaProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = ('numero','nombre')