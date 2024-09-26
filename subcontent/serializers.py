from liquor.models import Liquor
from cocktail.models import Cocktail
from rest_framework import serializers


class LiquorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liquor
        fields = ['name', 'taste', 'abv', 'price']


class CocktailDataSerializer(serializers.ModelSerializer):
    class Meata:
        model = Cocktail
        fields = ['name', 'ingredients', 'taste', 'abv']
