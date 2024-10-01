from django.shortcuts import render
from rest_framework.views import APIView
from .models import Info
from .serializers import InfoSerializer
from random import randint, sample
from cocktail.models import Cocktail
from cocktail.serializers import CocktailListSerializer
from rest_framework.response import Response
from rest_framework import status
from liquor.models import Liquor
from liquor.serializers import LiquorListSerializer
from django.db.models import Q
from rest_framework import pagination
# Create your views here.
class InfoAPIView(APIView):
    # info 생성
    def post(self,request):
        serializer = InfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"데이터 누락입니다."}, status=status.HTTP_400_BAD_REQUEST)

class MainPageAPIView(APIView):
    def get(self,request):
        reponse_seri = {}
        # info 전체 데이터 가져오기
        info = Info.objects.all()
        # info 전체 크기
        max_num = len(info)
        info = info[randint(0,max_num-1)]
        serializers = InfoSerializer(info)
        reponse_seri['info'] = serializers.data
        cocktail = Cocktail.objects.all()
        cocktail_list = cocktail.filter(id__in=sample(range(1,len(cocktail)),3)) 
        serializers2 = CocktailListSerializer(cocktail_list,many=True)
        reponse_seri['cocktail_list'] = serializers2.data
        # 사용자 맞춤 추천 기능 구현 해야함!!!!!!

        return Response(reponse_seri,status=status.HTTP_200_OK)

# 검색 기능
class SearchAPIView(APIView):
    def get(self,request):
        message = request.data.get("message")
        items = {}
        liquor_list = Liquor.objects.filter(Q(name__icontains=message) | Q(classification__icontains = message)).distinct()
        items['liquor_list'] = LiquorListSerializer(liquor_list, many=True).data
        cocktail_list = Cocktail.objects.filter(Q(name__icontains=message)).distinct()
        items['cocktail_list'] = CocktailListSerializer(cocktail_list, many=True).data
        if not items:
            return Response({"message":"검색된 결과가 없습니다."}, status=status.HTTP_200_OK) # 상태코드 확인해야 함!!!!!!!
        return Response(items,status=status.HTTP_200_OK)



# 페이지네이션
class RecordPagination(pagination.CursorPagination):
    page_size = 10
    ordering = "-created_at"
    cursor_query_param = "cursor"

    def get_paginated_response(self, data):
        return Response(
            {
                "meta": {"code": 200, "message": "OK"},
                "data": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "records": data,
                },
            },
            status=status.HTTP_200_OK,
        )