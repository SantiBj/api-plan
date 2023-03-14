from rest_framework import serializers
from modelosBase.models import Competencia

class CompetenciasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        fields = ('pk','nombre')