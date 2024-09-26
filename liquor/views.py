from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Liquor
from .serializers import LiquorListSerializer, LiquorDetailSerializer


# 주류 목록 조회(GET/ 누구나 이용 가능) 및 등록(POST/ 관리자만 가능)
class LiquorListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증된 회원(회원or관리자)만 가능 or 누구나 이용 가능

    # 주류 목록 조회
    def get(self, request):
        liquor = Liquor.objects.all()
        serializer = LiquorListSerializer(liquor, many=True)
        return Response(serializer.data)

    # 게시글 등록
    def post(self, request):
        #관리자인지 확인하는 코드 추가
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LiquorDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 북마크 기능(POST/ 회원만 가능)
class LiquorBookmarkView(APIView):
    permission_classes = [IsAuthenticated]  # 회원만 가능

    def post(self, request, pk):
        liquor = get_object_or_404(Liquor, pk=pk)
        user = request.user

        if user in liquor.bookmark.all():
            liquor.bookmark.remove(request.user)
            return Response({"message": "북마크 취소"}, status=status.HTTP_200_OK)
        else:
            liquor.bookmark.add(request.user)
            return Response({"message": "북마크 완료"}, status=status.HTTP_201_CREATED)


# 주류 디테일 페이지 조회(GET/누구나 이용 가능) 및 수정(PUT/관리자만), 삭제(DELETE/관리자만)
class LiquorDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증된 회원(회원or관리자)만 가능 or 누구나 이용 가능

    # 주류 디테일 페이지 조회
    def get(self, request, pk):
        liquor = get_object_or_404(Liquor, pk=pk)
        serializer = LiquorDetailSerializer(liquor)
        return Response(serializer.data)

    # 게시글 수정
    def put(self, request, pk):
        liquor = get_object_or_404(Liquor, pk=pk)
        #관리자인지 확인하는 코드 추가
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)
        

        serializer = LiquorDetailSerializer(liquor, data=request.data, partial=True)  # partial은 부분 수정
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, pk):
        liquor = get_object_or_404(Liquor, pk=pk)
        #관리자인지 확인하는 코드 추가
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)
        

        liquor.delete()
        return Response({"message": "게시글 삭제 완료"}, status=status.HTTP_403_FORBIDDEN)
