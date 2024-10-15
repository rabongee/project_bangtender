from django.shortcuts import render
from rest_framework.views import APIView
from .models import Info
from .serializers import InfoSerializer
from random import choice, sample
from cocktail.models import Cocktail
from cocktail.serializers import CocktailListSerializer
from rest_framework.response import Response
from rest_framework import status
from liquor.models import Liquor
from liquor.serializers import LiquorListSerializer
from django.db.models import Q
from rest_framework import pagination

from rest_framework.permissions import IsAuthenticated
from accounts.models import MyLiquor
from .functions import btd_bot
from django.core.cache import cache
# Create your views here.


class InfoAPIView(APIView):
    # info 생성
    def post(self, request):
        serializer = InfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "데이터 누락입니다."}, status=status.HTTP_400_BAD_REQUEST)


class MainPageAPIView(APIView):
    def get(self, request):
        response_seri = {}

        # info 랜덤 데이터 가져오기
        try:
            random_info = InfoSerializer(choice(Info.objects.all())).data
        except (IndexError):
            # info 데이터 없을시
            random_info = {'아직 알려드릴 정보가 없네요'}
        response_seri['info'] = random_info

        # 랜덤 칵테일 데이터 3개 하루에 한번 가져오기
        cocktail_cache_key = 'random_cocktail_list'
        random_cocktail_list = cache.get(cocktail_cache_key)
        if not random_cocktail_list:
            # 칵테일 데이터가 없으면 빈 데이터
            try:
                random_cocktail_list = CocktailListSerializer(
                    sample(list(Cocktail.objects.all()), 3), many=True
                ).data
                cache.set(cocktail_cache_key, random_cocktail_list,
                          timeout=86400)  # 24시간 (하루) 캐시 저장
            except (IndexError):
                response_seri['cocktail_list'] = {
                    '데이터 베이스에 칵테일 데이터가 3개 미만입니다. 데이터를 더 넣어주세요.'}
        response_seri['cocktail_list'] = random_cocktail_list

        # 로그인 안되었으면
        if not request.user.id:
            return Response(response_seri, status=status.HTTP_200_OK)

        # 사용자 맞춤 추천 데이터 가져오기
        liquor_list = MyLiquor.objects.filter(
            user_id=request.user.id
        ).prefetch_related("liquor", "user")

        # 가진 술 및 좋아하는 술 이름
        own_like_liquor = set(
            [i.liquor.name for i in liquor_list.filter(status__in=[
                "1", "2"])]
        )
        own_like_classification = set(
            [i.liquor.classification for i in liquor_list.filter(status__in=[
                "1", "2"])]
        )
        # 가진 술 및 좋아하는 술이 없으면
        if not own_like_liquor:
            response_seri['user_liquor_list'] = '사용자 데이터가 등록되지 않았습니다.'
            return Response(response_seri, status=status.HTTP_200_OK)

        # 랜덤 사용자 맞춤 칵테일 데이터 3개 가져오기, 하루에 한번
        # 가지고 있거나 좋아하는 술이 들어간 칵테일 혹은 같은 classification이 들어간 칵테일 랜덤으로 가져옴
        liquor_cache_key = f'random_custom_liquor_{request.user.id}'
        random_custom_liquor = cache.get(liquor_cache_key)

        try:
            # 캐시에 등록된 데이터가 없으면
            if not random_custom_liquor:
                # 기주 쿼리
                liquor_query = Q()
                for keyword in own_like_liquor:
                    liquor_query |= Q(ingredients__icontains=keyword)

                # 분류 쿼리
                classification_query = Q()
                for keyword in own_like_classification:
                    classification_query |= Q(ingredients__icontains=keyword)

                random_custom_liquor = sample(
                    list(
                        Cocktail.objects.filter(
                            liquor_query | classification_query)
                    ),
                    3
                )
                cache.set(liquor_cache_key, random_custom_liquor,
                          timeout=86400)  # 24시간 (하루) 캐시 저장
            response_seri['user_liquor_list'] = CocktailListSerializer(
                random_custom_liquor, many=True).data
        except (IndexError):
            response_seri["user_liquor_list"] = '사용자 맞춤으로 추천할 칵테일이 없네요...ㅠㅠ'
        return Response(response_seri, status=status.HTTP_200_OK)

# 검색 기능


class SearchAPIView(APIView):
    def get(self, request):
        message = request.query_params.get("message")
        # 검색어 입력 하지 않았을 때
        if not message:
            return Response({"message": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
        items = {}
        liquor_list = Liquor.objects.filter(Q(name__icontains=message) | Q(
            classification__icontains=message)).distinct()
        items['liquor_list'] = LiquorListSerializer(
            liquor_list, many=True).data
        cocktail_list = Cocktail.objects.filter(
            Q(name__icontains=message)).distinct()
        items['cocktail_list'] = CocktailListSerializer(
            cocktail_list, many=True).data
        if not items:
            return Response({"message": "검색된 결과가 없습니다."}, status=status.HTTP_200_OK)
        return Response(items, status=status.HTTP_200_OK)


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


class UserAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.address:
            return Response({"address": user.address})
        else:
            return Response({
                "message": "주소가 등록되어 있지 않습니다."
            }, status=status.HTTP_400_BAD_REQUEST)


class BangtenderBot(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 유효성 검증
        if request.user.id is None:
            return Response({"message": "user_id가 누락됐습니다."}, status=status.HTTP_400_BAD_REQUEST)

        message = request.data.get("message")  # 유저가 입력한 message

        # OpenAI와 소통했던 내역이 저장된 히스토리
        history = request.data.get("history", [])

        # 처음 질문을 받는 것이라면 system prompt에 사용자 정보를 넘겨줘야 하므로 데이터베이스 접근.
        user_liquor = []
        like_liquor = []
        hate_liquor = []
        if len(history) == 0:
            liquor_list = MyLiquor.objects.filter(
                user_id=request.user.id).prefetch_related("liquor", "user")
            user_liquor = [i.liquor.name for i in liquor_list.filter(
                status="1")]  # 내가 가진 술
            like_liquor = [i.liquor.name for i in liquor_list.filter(
                status="2")]  # 내가 좋아하는 술
            hate_liquor = [i.liquor.name for i in liquor_list.filter(
                status="3")]  # 내가 싫어하는 술
        new_history = btd_bot(message, message_history=history,
                              user_liquor=user_liquor, like_liquor=like_liquor, hate_liquor=hate_liquor
                              )
        print(new_history[-1]['content'])
        return Response(new_history, status=status.HTTP_200_OK)


# NEWMODULE: 파인튜닝 모델
# 파인튜닝 함수
# class MyFineTuning(APIView):
#     def post(self, request):
#         # 파인튜닝은 관리자 권한만 가능함
#         if not request.user.is_superuser:
#             return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)

#         # 파인튜닝할 데이터 생성
#         data = pre_data()
#         client = OpenAI(api_key=openai_api_key)
#         # 데이터 jsonl로 생성
#         with open('web_database.jsonl', 'w', encoding='utf-8') as f:
#             for entry in data:
#                 json.dump(entry, f, ensure_ascii=False)
#                 f.write('\n')

#         # JSON 포맷 데이터 검증 코드
#         with open('web_database.jsonl', 'r', encoding='utf-8') as f:
#             for i, line in enumerate(f):
#                 try:
#                     json.loads(line)
#                     print("JSON 형태 오류 없음")
#                 except json.JSONDecodeError as e:
#                     print(f"{i+1}번째 줄에서 JSONDecodeError 발생: {e}")

#         # 생성 파일 OpenAI 업로드
#         training_response = client.files.create(
#             file=open('web_database.jsonl', 'rb'),
#             purpose='fine-tune'
#         )

#         training_file_id = training_response.id
#         print(f"업로드 파일 ID: {training_file_id}")

#         # 파인튜닝 작업 생성
#         fine_tune_response = client.fine_tuning.jobs.create(
#             training_file=training_file_id,
#             # 3.5 모델 사용시 1106 모델 사용을 추천함. (타 모델 사용 시 승인지연 등 이슈가 많음)
#             model="gpt-3.5-turbo-1106"
#         )
#         fine_tune_job_id = fine_tune_response.id
#         print(f"파인튜닝 작업 ID: {fine_tune_job_id}")

#         # 파인튜닝 작업 상태 확인
#         progress = ''
#         while progress != 'succeeded':
#             fine_tune_job = client.fine_tuning.jobs.retrieve(fine_tune_job_id)
#             progress = fine_tune_job.status
#             print(f"파인튜닝 상태: {progress}")
#             if progress == 'succeeded':
#                 print("파인튜닝이 완료되었습니다.")
#                 break
#             elif progress == 'failed':
#                 print("파인튜닝에 실패했습니다.")
#                 print(f"오류 내용: {fine_tune_job}")
#                 break
#             time.sleep(30)
#         fine_tuned_model = fine_tune_job.fine_tuned_model
#         print(f"파인튜닝된 모델 이름: {fine_tuned_model}")
#         return Response({f"message: {progress}"}, status=status.HTTP_201_CREATED)

#     # OpenAI delete 기능 이슈 있음.(모델 찾을수 없다는 OpenAI 쪽 문제)
#     def delete(self, request):
#         if not request.user.is_superuser:
#             return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)
#         client = OpenAI(api_key=openai_api_key)
#         # 삭제할 파인튜닝 모델 이름
#         client.Model.delete(request.data)
#         return Response({"message": "삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
