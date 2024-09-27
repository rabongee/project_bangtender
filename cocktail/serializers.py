from rest_framework import serializers
from .models import Cocktail

class CocktailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cocktail
        fields = ['id', 'name', 'img']

class CocktailDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cocktail
        fields = ['id', 'name', 'img', 'content', 'ingredients', 'taste', 'abv',  'created_at', 'updated_at']