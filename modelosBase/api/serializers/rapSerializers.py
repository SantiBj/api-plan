from rest_framework import serializers
from modelosBase.models import Rap


class RapNoAsignadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rap
        fields = '__all__'

    