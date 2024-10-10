from rest_framework import serializers
from .models import User, MyLiquor


class MyLiquorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyLiquor
        fields = ['id', 'liquor', 'status']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "name", "email", "address"
        ]


class UserLiquorSerializer(serializers.ModelSerializer):
    my_liquors = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'my_liquors',
                  "name", "address", "is_superuser"]

    def get_my_liquors(self, obj):
        my_liquors = MyLiquor.objects.filter(user=obj)
        return {
            'owned': MyLiquorSerializer(my_liquors.filter(status='1'), many=True).data,
            'favorite': MyLiquorSerializer(my_liquors.filter(status='2'), many=True).data,
            'disliked': MyLiquorSerializer(my_liquors.filter(status='3'), many=True).data,
        }
