from rest_framework import serializers
from .models import Liquor


class LiquorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liquor
        fields = [
            "id",
            "name",
            "price",
            "img",
        ]
# postman에서 조회하기 어려워 id 임시 추가!!!

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
