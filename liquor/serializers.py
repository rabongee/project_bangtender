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

    def __init__(self, *args, **kwargs):
        # kwargs에 'exclude_fields' 인자를 받는 경우 해당 필드를 제외
        exclude_fields = kwargs.pop('exclude_fields', None)
        super().__init__(*args, **kwargs)

        if exclude_fields:
            for field in exclude_fields:
                self.fields.pop(field)


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
