import bcrypt
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User, MyLiquor
from .validators import (
    validator_signup, validator_update_user, validator_change_password)
from .serializers import UserSerializer, UserLiquorSerializer
from liquor.models import Liquor
from liquor.serializers import LiquorListSerializer
from cocktail.models import Cocktail
from cocktail.serializers import CocktailListSerializer


class AccountView(APIView):
    """회원가입 및 회원탈퇴 APIView

    * POST
    비로그인 유저도 접근 가능

    * DELETE
    로그인한 유저만 가능
    """

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def post(self, request):
        is_valid, error_message = validator_signup(request.data)
        if not is_valid:
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=request.data.get("username"),
            password=request.data.get("password"),
            name=request.data.get("name"),
            email=request.data.get("email"),
            address=request.data.get("address"),
        )
        serializer = UserSerializer(user)
        res_data = serializer.data
        refresh = RefreshToken.for_user(user)
        res_data['refresh_token'] = str(refresh)
        res_data['access_token'] = str(refresh.access_token)
        return Response(res_data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        password = request.data.get('password')
        user = request.user
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return Response({"message": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        user.soft_delete()
        return Response({"message": "회원탈퇴에 성공했습니다."})


class LoginView(APIView):
    """로그인 APIView

    * POST
    비로그인 유저도 접근 가능
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            return Response({"message": "아이디가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({"message": "회원 정보가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            serializer = UserSerializer(user)
            res_data = serializer.data
            refresh = RefreshToken.for_user(user)
            res_data['refresh_token'] = str(refresh)
            res_data['access_token'] = str(refresh.access_token)
            return Response(res_data)
        else:
            return Response({"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """로그아웃 APIView

    * post
    로그인한 유저만 가능
    """

    def post(self, request):
        refresh_token_str = request.data.get("refresh_token")
        try:
            refresh_token = RefreshToken(refresh_token_str)
        except TokenError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token.blacklist()
        return Response({"message": "성공적으로 로그아웃 되었습니다."})


class ChangePasswordView(APIView):
    """비밀번호 변경 APIView

    * PUT
    로그인한 유저만 가능
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            is_valid, error_message = validator_change_password(
                request.data, user)
            if not is_valid:
                return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

            new_password = request.data.get('new_password')
            hashed_password = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt())
            user.password = hashed_password.decode("utf-8")
            user.save()
            return Response({"message": "패스워드 변경에 성공했습니다."})
        else:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class UserAPIView(APIView):
    """회원정보 APIView

    * GET
    로그인한 유저만 사용가능

    * PUT
    로그인한 유저만 사용가능
    """

    permission_classes = [IsAuthenticated]

    def get_user_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_user_object(pk)
        liquor = Liquor.objects.all()
        if user == request.user:
            res_data = {}
            user_serializer = UserLiquorSerializer(user)
            liquor_serializer = LiquorListSerializer(
                liquor, exclude_fields=["price", "img"], many=True)
            res_data['user_data'] = user_serializer.data
            res_data['liquor_data'] = liquor_serializer.data
            return Response(res_data)
        else:
            return Response({"message": "로그인한 유저와 다릅니다."}, status=status.HTTP_403_FORBIDDEN)

    # put 메소드 내의 작업을 하나의 트랜잭션으로 묶어서 하나의 단위로 처리됨
    # 중간에 오류 발생시 전체 롤백
    @transaction.atomic
    def put(self, request, pk):
        user = self.get_user_object(pk)
        if user == request.user:
            is_valid, error_message = validator_update_user(request.data, user)
            if not is_valid:
                return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserLiquorSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # 유저의 아이디를 가진 MyLiquor을 가져옴
                my_liquors_data = request.data.get('my_liquors', {})
                status_map = {'owned': '1', 'favorite': '2', 'disliked': '3'}

                """
                my_liquors_data에서 각 상태에 해당하는 술 목록을 순회하고
                기존의 술 목록과 새로운 술 목록을 비교
                """
                for status_key, liquors in my_liquors_data.items():
                    status_value = status_map.get(status_key)
                    if status_value:
                        existing_liquors = MyLiquor.objects.filter(
                            user=user, status=status_value)
                        existing_ids = set(
                            existing_liquors.values_list('liquor_id', flat=True))
                        new_ids = set(liquors)

                        # 새로운 술 id가 기존 술 id에 없으면 추가
                        ids_to_add = new_ids - existing_ids
                        for liquor_id in ids_to_add:
                            MyLiquor.objects.create(
                                user=user, liquor_id=liquor_id, status=status_value)

                        # 기존 술 id중 새로운 술 id에 포함되지 않으면 데이터베이스에서 삭제
                        ids_to_remove = existing_ids - new_ids
                        MyLiquor.objects.filter(
                            user=user, liquor_id__in=ids_to_remove, status=status_value).delete()

                return Response(UserLiquorSerializer(user).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "수정 권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)


class MyBookmarkListView(APIView):
    """내 북마크 APIView

    * GET
    로그인한 유저만 가능
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            res_data = {}
            liquor = Liquor.objects.filter(bookmark__id=pk)
            serializer = LiquorListSerializer(liquor, many=True)
            res_data['liquor'] = serializer.data
            cocktail = Cocktail.objects.filter(
                bookmark__id=pk)
            serializer = CocktailListSerializer(cocktail, many=True)
            res_data['cocktail'] = serializer.data
            return Response(res_data)
        else:
            return Response({"message": "다른 사람의 북마크는 볼 수 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)
