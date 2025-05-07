from rest_framework import serializers

from inventaire.models import *

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model=Stock
        fields='__all__'

class GroupeElectrogeneSerializer(serializers.ModelSerializer) :
    class Meta:
        model=GroupeElectrogene
        fields='__all__'       

class CabinesAutonomeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CabinesAutonome
        fields='__all__'

class ModulaireSerializer(serializers.ModelSerializer):
    class Meta:
        model=Modulaire
        fields='__all__'

# serializer of Movements
class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movement
        fields='__all__'