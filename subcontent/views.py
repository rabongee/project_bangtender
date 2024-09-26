import time
import json
from openai import OpenAI
from config import openai_api_key
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework.views import APIView
from accounts.models import User, My_Liquor
from liquor.models import Liquor
from cocktail.models import Cocktail
from serializers import LiquorDataSerializer, CocktailDataSerializer
from functions import btd_bot

### bangtenderbot 함수용 serializers를 따로 만듦 ###

# class fine_tuning으로 파인튜닝하는 클래스 만들고, 만들어진 파인튜닝 모델 가져다가 쓰는 클래스를 따로 만들어야함.(2개)


class MyFineTuning(APIView):
    permission_classes = [IsAdminUser]  # 파인튜닝은 관리자 권한만 가능함

    def post(self, request):
        query_liquor = Liquor.objects.all()
        query_cocktail = Cocktail.objects.all()

        # 커스텀 serializer로 필요한 정보들만 담아서 serializer한 후, 데이타 추출해서 텍스트로 저장
        liquor_data = json.dumps(LiquorDataSerializer(
            query_liquor, many=True).data, ensure_ascii=False)
        cocktail_data = json.dumps(CocktailDataSerializer(
            query_cocktail, many=True).data, ensure_ascii=False)

        client = OpenAI(api_key=openai_api_key)

        # 데이터 준비 (나만의 레시피 업로드, 현재는 10개정도 지정 / 파인튜닝에는 최소 10개 필요 / 토큰 유의)
        data = [
            {
                "messages": [
                    {"role": "system",
                        "content": f"당신은 데이터 {liquor_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "싱글몰트 위스키로 만들 수 있는 칵테일은 무엇인가요?"},
                    {"role": "assistant",
                        "content": "올드 패션드를 만들 수 있습니다. 싱글몰트 위스키, 설탕, 비터스를 사용합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "집에 보드카가 있는데 어떤 칵테일을 만들 수 있나요?"},
                    {"role": "assistant",
                        "content": "모스크바 뮬을 만들 수 있습니다. 보드카, 라임 주스, 진저 비어를 사용합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "럼주로 만들 수 있는 다른 칵테일 추천해줘"},
                    {"role": "assistant",
                        "content": "다이키리를 만들어 보세요. 럼주, 라임 주스, 설탕이 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "테킬라로 어떤 칵테일을 만들 수 있나요?"},
                    {"role": "assistant",
                        "content": "마가리타를 만들 수 있습니다. 테킬라, 라임 주스, 트리플 섹이 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "집에 진과 토닉 워터가 있어. 뭐 만들 수 있을까?"},
                    {"role": "assistant", "content": "진 토닉을 만들 수 있습니다. 진과 토닉 워터를 섞어주세요."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "버번 위스키로 추천하는 칵테일 있어?"},
                    {"role": "assistant",
                        "content": "맨해튼을 만들어 보세요. 버번 위스키, 스위트 베르무트, 비터스가 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "와인으로 만들 수 있는 칵테일 있나요?"},
                    {"role": "assistant",
                        "content": "샹그리아를 만들어 보세요. 와인, 과일, 브랜디, 주스가 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "트리플 섹이 있는데 뭘 만들 수 있을까?"},
                    {"role": "assistant",
                        "content": "사이드카를 만들 수 있습니다. 트리플 섹, 코냑, 레몬 주스가 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "샴페인으로 칵테일 만들 수 있어?"},
                    {"role": "assistant", "content": "벨리니를 만들어 보세요. 샴페인과 복숭아 퓌레가 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "칼루아가 있는데 칵테일 추천해줘"},
                    {"role": "assistant",
                        "content": "화이트 러시안을 만들 수 있습니다. 칼루아, 보드카, 우유가 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "아마레또로 뭐 만들 수 있나요?"},
                    {"role": "assistant",
                        "content": "아마레또 사워를 만들어 보세요. 아마레또, 레몬 주스, 설탕 시럽이 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "집에 코코넛 럼이 있는데 사용할 수 있는 칵테일 있어?"},
                    {"role": "assistant",
                        "content": "피나 콜라다를 만들어 보세요. 코코넛 럼, 파인애플 주스, 코코넛 크림이 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "위스키와 레몬 주스가 있는데 어떤 칵테일을 만들 수 있나요?"},
                    {"role": "assistant",
                        "content": "위스키 사워를 만들 수 있습니다. 위스키, 레몬 주스, 설탕 시럽을 사용합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "집에 민트 리큐어가 있어. 추천하는 칵테일 있니?"},
                    {"role": "assistant",
                        "content": "그래스호퍼를 만들어 보세요. 민트 리큐어, 초콜릿 리큐어, 우유가 필요합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술을 기반으로 칵테일 레시피를 제공하는 도움이 되는 어시스턴트입니다."},
                    {"role": "user", "content": "애플 브랜디로 만들 수 있는 칵테일은?"},
                    {"role": "assistant",
                        "content": "잭 로즈를 만들어 보세요. 애플 브랜디, 레몬 주스, 그레나딘이 필요합니다."}
                ]
            }
        ]

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
        status = ''
        while status != 'succeeded':
            fine_tune_job = client.fine_tuning.jobs.retrieve(fine_tune_job_id)
            status = fine_tune_job.status
            print(f"파인튜닝 상태: {status}")
            if status == 'succeeded':
                print("파인튜닝이 완료되었습니다.")
                break
            elif status == 'failed':
                print("파인튜닝에 실패했습니다.")
                print(f"오류 내용: {fine_tune_job}")
                break
            time.sleep(30)


class BangtenderBot(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # # 유효성 검증
        # is_valid, error_message = validate_talk(request.data)
        # if not is_valid:
        #     return Response(f"{error_message}", status=status.HTTP_400_BAD_REQUEST)

        message = request.data.get("message")  # 유저가 입력한 message
        # OpenAI와 소통했던 내역이 저장된 히스토리/ json 형태로 받나?
        history = request.data.get("history")

        # 함수에 넣기위한 초기화
        liquor_data1 = ""
        liquor_data2 = ""
        liquor_data3 = ""
        # 처음 질문을 받는 것이라면 system prompt에 사용자 정보를 넘겨줘야 하므로 데이터베이스 접근.
        if len(history) == 0:
            liquor_list = My_Liquor.objects.filter(
                user_id=request.user.id).prefetch_related("my_liquor", "my_user")
            liquor_data1 = json.dumps(LiquorDataSerializer(liquor_list.filter(
                status="1"), many=True).data, ensure_ascii=False)  # 내가 가진 술
            liquor_data2 = json.dumps(LiquorDataSerializer(liquor_list.filter(
                status="2"), many=True).data, ensure_ascii=False)  # 내가 좋아하는 술
            liquor_data3 = json.dumps(LiquorDataSerializer(liquor_list.filter(
                status="3"), many=True).data, ensure_ascii=False)  # 내가 싫어하는 술

        # 딕셔너리 형태로 받았기에 json으로 변환해서 보내야함.
        new_history = btd_bot(message, message_history=history,
                              liquor1=liquor_data1, liquor2=liquor_data2, liquor3=liquor_data3)
        return json.dumps(new_history, ensure_ascii=False)
