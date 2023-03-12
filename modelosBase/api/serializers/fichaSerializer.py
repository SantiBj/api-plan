from rest_framework import serializers
from modelosBase.models import Ficha

# fichas pertencientes a un programa

class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = ('numero','nombre')

class CrearFichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha 
        fields = '__all__'