import bcrypt
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
from .validators import validator_signup, validator_update_user
from .serializers import UserSerializer


class AccountView(APIView):
    def post(self, request):
        is_valid, error_message = validator_signup(request.data)
        if not is_valid:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

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


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            return Response({"error": "아이디가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            serializer = UserSerializer(user)
            res_data = serializer.data
            refresh = RefreshToken.for_user(user)
            res_data['refresh_token'] = str(refresh)
            res_data['access_token'] = str(refresh.access_token)
            return Response(res_data)
        else:
            return Response({"error": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token_str = request.data.get("refresh_token")
        try:
            refresh_token = RefreshToken(refresh_token_str)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token.blacklist()
        return Response({"message": "성공적으로 로그아웃 되었습니다."})


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_object(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request, username):
        user = self.get_user_object(username)
        if user == request.user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"message": "로그인한 유저와 다릅니다."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, username):
        user = self.get_user_object(username)
        if user == request.user:
            is_valid, error_message = validator_update_user(request.data, user)
            if not is_valid:
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

        else:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
