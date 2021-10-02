from rest_framework import serializers
from webapp.models import liga,equipo,jugador

class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model=liga
        fields=('id', 'sport', 'name', 'teams', 'players', 'self',
        )
LigaSerializer._declared_fields["self"] = serializers.CharField(source="_self")

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model=equipo 
        fields=('id', 'liga_id', 'name', 'city','league', 'players', 'self',
        )
EquipoSerializer._declared_fields["self"] = serializers.CharField(source="_self")

class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model=jugador
        fields=('id', 'equipo_id', 'name', 'age','position', 'time_trained', 'league', 'team', 'self',
        )
JugadorSerializer._declared_fields["self"] = serializers.CharField(source="_self")
