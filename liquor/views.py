from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Liquor
from .serializers import LiquorListSerializer, LiquorDetailSerializer


# 주류 목록 조회(GET/ 누구나 이용 가능) 및 등록(POST/ 관리자만 가능)
class LiquorListView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 관리자만 가능 or 누구나 이용 가능

    def get(self, request):
        liquors = Liquor.objects.all()
        serializer = LiquorListSerializer(liquors, many=True)
        return Response(serializer.data)

    # def post(self, request):
        
    #     serializer=LiquorListSerializer(data=request.data)


# 주류 디테일 페이지 조회(GET/누구나 이용 가능)
class LiquorDetailView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 관리자만 가능 or 누구나 이용 가능

    def get(self, request,id):
        get_object_or_404(Liquor, id=id)
        serializer = LiquorDetailSerializer(liquors)
        return Response(serializer.data)

    # 수정, 삭제를 여기에 해야하지 않을까
