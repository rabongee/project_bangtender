from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Liquor
from .serializers import LiquorListSerializer, LiquorDetailSerializer
from subcontents.views import RecordPagination
from rest_framework.generics import ListCreateAPIView
from liquor.validators import validator_liquor
from django.db.models import Q


class LiquorListView(ListCreateAPIView):
    """주류 게시글 조회 및 등록 APIView

    * GET
    비로그인 유저도 접근 가능

    * POST
    superuser만 가능

    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = LiquorListSerializer
    pagination_class = RecordPagination

    #
    def get_queryset(self):
        liquor = Liquor.objects.all()
        classification = self.request.query_params.get('classification', 'all')
        if classification == 'others':
            liquor = liquor.exclude(
                Q(classification='위스키') | Q(classification='진') | Q(classification='럼') | Q(classification='보드카') | Q(classification='리큐르') | Q(classification='브랜디'))
        elif classification != 'all':
            liquor = liquor.filter(classification=classification)
        return liquor

    def get(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        if request.user:
            response.data['is_superuser'] = request.user.is_superuser
        return Response(response.data)

    def post(self, request):
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)

        is_valid, error_message = validator_liquor(request.data)
        if not is_valid:
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LiquorDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LiquorBookmarkView(APIView):
    """Liquor Bookmark APIView
    
    * POST
    로그인 한 유저만 가능
    """
    
    permission_classes = [IsAuthenticated]  # 회원만 가능

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"detail": "회원만 이용 가능합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        liquor = get_object_or_404(Liquor, pk=pk)
        user = request.user

        if user in liquor.bookmark.all():
            liquor.bookmark.remove(request.user)
            return Response({"message": "북마크 취소"}, status=status.HTTP_200_OK)
        else:
            liquor.bookmark.add(request.user)
            return Response({"message": "북마크 완료"}, status=status.HTTP_201_CREATED)


class LiquorDetailView(APIView):
    """Liquor 상세 페이지 조회, 수정 및 삭제
    
    * GET
    비로그인 유저도 이용가능

    * PUT
    superuser만 가능

    * DELETE
    superuser만 가능
    """
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        liquor = get_object_or_404(Liquor, pk=pk)
        serializer = LiquorDetailSerializer(liquor)
        res_data = serializer.data
        if request.user:
            res_data['is_superuser'] = request.user.is_superuser
        return Response(res_data)

    def put(self, request, pk):
        liquor = get_object_or_404(Liquor, pk=pk)
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)

        is_valid, error_message = validator_liquor(
            request.data, liquor_instance=liquor)
        if not is_valid:
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LiquorDetailSerializer(
            liquor, data=request.data, partial=True)  # partial은 부분 수정
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        liquor = get_object_or_404(Liquor, pk=pk)
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)

        liquor.delete()
        return Response({"message": "게시글 삭제 완료"})
