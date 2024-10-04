from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from cocktail.validators import validator_cocktail
from .models import Cocktail
from .serializers import CocktailListSerializer, CocktailDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from subcontents.views import RecordPagination
from rest_framework.generics import ListAPIView


# 칵테일 목록 조회(GET/ 누구나 이용 가능) 및 등록(POST/ 관리자만 가능)
class CocktailListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 칵테일 목록 조회
    serializer_class = CocktailListSerializer
    pagination_class = RecordPagination
    def get_queryset(self):
        cocktail = Cocktail.objects.all()
        return cocktail

    # 게시글 등록
    def post(self, request):
        # 관리자 확인 코드
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)

        # 검증 로직
        is_valid, error_message = validator_cocktail(request.data)
        if not is_valid:
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CocktailDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 북마크 기능(POST/ 회원만 가능)
class CocktailBookmarkView(APIView):
    permission_classes = [IsAuthenticated]  # 회원만 가능

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"detail": "회원만 이용 가능합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        cocktail = get_object_or_404(Cocktail, pk=pk)
        user = request.user

        if user in cocktail.bookmark.all():
            cocktail.bookmark.remove(request.user)
            return Response({"message": "북마크 취소"}, status=status.HTTP_200_OK)
        else:
            cocktail.bookmark.add(request.user)
            return Response({"message": "북마크 완료"}, status=status.HTTP_201_CREATED)



# 칵테일 디테일 페이지 조회(GET/누구나 이용 가능) 및 수정(PUT/관리자만), 삭제(DELETE/관리자만)
class CocktailDetailView(APIView):
    # 인증된 회원(회원or관리자)만 가능 or 누구나 이용 가능

    permission_classes = [IsAuthenticatedOrReadOnly]

    # 칵테일 디테일 페이지 조회
    def get(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        serializer = CocktailDetailSerializer(cocktail)
        return Response(serializer.data)

    # 게시글 수정
    def put(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        # 관리자 확인 코드
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)

        # 검증 로직
        is_valid, error_message = validator_cocktail(request.data, cocktail_instance=cocktail)
        if not is_valid:
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CocktailDetailSerializer(
            cocktail, data=request.data, partial=True)  # partial은 부분 수정
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, pk):
        cocktail = get_object_or_404(Cocktail, pk=pk)
        # 관리자 확인 코드
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)

        cocktail.delete()
        return Response({"message": "게시글 삭제 완료"}, status=status.HTTP_403_FORBIDDEN)

