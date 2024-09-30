from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Cocktail
from .serializers import CocktailListSerializer, CocktailDetailSerializer
from rest_framework.exceptions import ValidationError

# 칵테일 목록 조회 및 추가


class CocktailListCreateView(generics.ListCreateAPIView):
    queryset = Cocktail.objects.all()
    serializer_class = CocktailListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        serializer = CocktailDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "데이터 누락입니다."}, status=status.HTTP_400_BAD_REQUEST)

# 칵테일 상세 조회, 수정 및 삭제


class CocktailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cocktail.objects.all()
    serializer_class = CocktailDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# 북마크 기능 (POST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmark_cocktail(request, pk):
    try:
        cocktail = Cocktail.objects.get(pk=pk)
    except Cocktail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user in cocktail.bookmark.all():
        cocktail.bookmark.remove(user)
        bookmarked = "북마크 취소"
    else:
        cocktail.bookmark.add(user)
        bookmarked = "북마크 완료"

    return Response({'message': bookmarked})
