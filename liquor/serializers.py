from rest_framework import serializers
from .models import Liquor


class LiquorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liquor
        fields = [
            "name",
            "price",
            "img",
        ]


class LiquorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liquor
        fields = [
            "name",
            "classification",
            "img",
            "content",
            "taste",
            "abv",
            "price",
        ]  # 모델의 모든 필드를 직렬화
