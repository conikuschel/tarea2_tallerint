from rest_framework import serializers
from webapp.models import liga,equipo,jugador

class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model=liga
        fields='__all__'

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model=equipo 
        fields='__all__'

class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model=jugador
        fields='__all__'