from rest_framework import serializers
from usuarioBase.models import Instructor

class ListaInstructoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ("documento","nombreCompleto")

class CrearInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'

    # editando el metodo save para que encripte la contraseña
    def create(self, validated_data):
        print(validated_data)
        instructor = Instructor(**validated_data)#asignando la data a cada atributo
        instructor.set_password(validated_data["password"])
        instructor.save()
        return instructor

