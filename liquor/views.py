from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    IsAuthenticated,
)
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Liquor
from .serializers import LiquorListSerializer, LiquorDetailSerializer


# 주류 목록 조회(GET/ 누구나 이용 가능) 및 등록(POST/ 관리자만 가능)
class LiquorListView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 관리자만 가능 or 누구나 이용 가능

    # 주류 목록 조회
    def get(self, request):
        liquors = Liquor.objects.all()
        serializer = LiquorListSerializer(liquors, many=True)
        return Response(serializer.data)

    # 게시글 등록
    def post(self, request):
        self.permission_classes = [IsAdminUser]  # 관리자만 등록 가능
        self.check_object_permissions(request)  # 관리자가 맞는지 체크
        serializer = LiquorDetailSerializer(data=request.data)
        if serializer.is_vaild():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 북마크 기능(POST/ 회원만 가능)
class LiquorBookmarkView(APIView):
    permission_classes = [IsAuthenticated]  # 회원만 가능

    def post(self, request, id):
        liquors = get_object_or_404(Liquor, pk=id)
        user = request.user

        if user in liquors.bookmark.all():
            liquors.bookmark.remove(request.user)
            return Response({"message": "북마크 취소"}, status=status.HTTP_200_OK)
        else:
            liquors.bookmark.add(request.user)
            return Response({"message": "북마크 완료"}, status=status.HTTP_201_CREATED)


# 주류 디테일 페이지 조회(GET/누구나 이용 가능) 및 수정(PUT/관리자만), 삭제(DELETE/관리자만)
class LiquorDetailView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 관리자만 가능 or 누구나 이용 가능

    # 주류 디테일 페이지 조회
    def get(self, request, id):
        liquors = get_object_or_404(Liquor, pk=id)
        serializer = LiquorDetailSerializer(liquors)
        return Response(serializer.data)

    # 게시글 수정
    def put(self, request, id):
        self.permission_classes = [IsAdminUser]  # 관리자만 등록 가능
        self.check_object_permissions(request)  # 관리자가 맞는지 체크
        liquors = get_object_or_404(Liquor, pk=id)
        serializer = LiquorDetailSerializer(liquors, data=request.data)
        if serializer.is_vaild():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, id):
        self.permission_classes = [IsAdminUser]  # 관리자만 등록 가능
        self.check_object_permissions(request)  # 관리자가 맞는지 체크
        liquors = get_object_or_404(Liquor, pk=id)
        liquors.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
