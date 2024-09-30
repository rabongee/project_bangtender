import time
import json
from openai import OpenAI
from config import openai_api_key
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import MyLiquor
from .functions import btd_bot, pre_data


class MyFineTuning(APIView):

    def post(self, request):
        # 파인튜닝은 관리자 권한만 가능함
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)

        # 파인튜닝할 데이터 생성
        data = pre_data()
        client = OpenAI(api_key=openai_api_key)
        # 데이터 jsonl로 생성
        with open('web_database.jsonl', 'w', encoding='utf-8') as f:
            for entry in data:
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n')

        # JSON 포맷 데이터 검증 코드
        with open('web_database.jsonl', 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                try:
                    json.loads(line)
                    print("JSON 형태 오류 없음")
                except json.JSONDecodeError as e:
                    print(f"{i+1}번째 줄에서 JSONDecodeError 발생: {e}")

        # 생성 파일 OpenAI 업로드
        training_response = client.files.create(
            file=open('web_database.jsonl', 'rb'),
            purpose='fine-tune'
        )

        training_file_id = training_response.id
        print(f"업로드 파일 ID: {training_file_id}")

        # 파인튜닝 작업 생성
        fine_tune_response = client.fine_tuning.jobs.create(
            training_file=training_file_id,
            # 3.5 모델 사용시 1106 모델 사용을 추천함. (타 모델 사용 시 승인지연 등 이슈가 많음)
            model="gpt-3.5-turbo-1106"
        )
        fine_tune_job_id = fine_tune_response.id
        print(f"파인튜닝 작업 ID: {fine_tune_job_id}")

        # 파인튜닝 작업 상태 확인
        progress = ''
        while progress != 'succeeded':
            fine_tune_job = client.fine_tuning.jobs.retrieve(fine_tune_job_id)
            progress = fine_tune_job.status
            print(f"파인튜닝 상태: {progress}")
            if progress == 'succeeded':
                print("파인튜닝이 완료되었습니다.")
                break
            elif progress == 'failed':
                print("파인튜닝에 실패했습니다.")
                print(f"오류 내용: {fine_tune_job}")
                break
            time.sleep(30)
        fine_tuned_model = fine_tune_job.fine_tuned_model
        print(f"파인튜닝된 모델 이름: {fine_tuned_model}")
        return Response({f"message: {progress}"}, status=status.HTTP_201_CREATED)

    # chatgpt가 문제임 내 문제 아님

    def delete(self, request):

        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)

        client = OpenAI(api_key=openai_api_key)
        # 삭제할 파인튜닝 모델 이름
        # openai.Model.delete(request.data)
        client.models.delete("ft:gpt-3.5-turbo-1106:personal::AD31BXWl")
        return Response({"message": "삭제 성공"}, status=status.HTTP_204_NO_CONTENT)


class BangtenderBot(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # # 유효성 검증
        # is_valid, error_message = validate_talk(request.data)
        # if not is_valid:
        #     return Response(f"{error_message}", status=status.HTTP_400_BAD_REQUEST)

        message = request.data.get("message")  # 유저가 입력한 message

        # OpenAI와 소통했던 내역이 저장된 히스토리
        history = request.data.get("history")

        # 함수에 넣기위한 초기화
        liquor_data1 = []
        liquor_data2 = []
        liquor_data3 = []
        # 처음 질문을 받는 것이라면 system prompt에 사용자 정보를 넘겨줘야 하므로 데이터베이스 접근.
        if len(history) == 0:
            liquor_list = MyLiquor.objects.filter(
                user_id=request.user.id).prefetch_related("my_liquor", "my_user")
            liquor_data1 = list(liquor_list.filter(status="1"))  # 내가 가진 술
            liquor_data2 = list(liquor_list.filter(status="2"))  # 내가 좋아하는 술
            liquor_data3 = list(liquor_list.filter(status="3"))  # 내가 싫어하는 술

        # 딕셔너리 형태로 받았기에 json으로 변환해서 보내야함.
        new_history = btd_bot(message, message_history=history,
                              liquor1=liquor_data1, liquor2=liquor_data2, liquor3=liquor_data3)
        return json.dumps(new_history, ensure_ascii=False)
