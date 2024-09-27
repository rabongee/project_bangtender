import time
import json
from openai import OpenAI
from config import openai_api_key
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import MyLiquor
from liquor.models import Liquor
from cocktail.models import Cocktail
from .serializers import LiquorDataSerializer, CocktailDataSerializer
from .functions import btd_bot

### bangtenderbot 함수용 serializers를 따로 만듦 ###

# class fine_tuning으로 파인튜닝하는 클래스 만들고, 만들어진 파인튜닝 모델 가져다가 쓰는 클래스를 따로 만들어야함.(2개)


class MyFineTuning(APIView):

    def post(self, request):
        # 파인튜닝은 관리자 권한만 가능함
        if not request.user.is_superuser:
            return Response({"detail": "접근 불가 / 관리자만 가능"}, status=status.HTTP_403_FORBIDDEN)
        query_liquor = Liquor.objects.all()
        query_cocktail = Cocktail.objects.all()

        # 커스텀 serializer로 필요한 정보들만 담아서 serializer한 후, 데이타 추출해서 텍스트로 저장
        liquor_data = json.dumps(LiquorDataSerializer(
            query_liquor, many=True).data, ensure_ascii=False)
        cocktail_data = json.dumps(CocktailDataSerializer(
            query_cocktail, many=True).data, ensure_ascii=False)

        client = OpenAI(api_key=openai_api_key)

        # 데이터 준비 (나만의 레시피 업로드, 현재는 10개정도 지정 / 파인튜닝에는 최소 10개 필요 / 토큰 유의)
        ### 1차 목표는 술 추천 및 칵테일 추천기능 활성화 ###
        data = [
            {
                "messages": [
                    {"role": "system",
                        "content": "당신은 사용자의 가진 술로 만들 수 있는 칵테일이나 술을 추천해주는 어시스턴트입니다."},
                    {"role": "user", "content": "위스키 종류에는 무엇이 있니?"},
                    {"role": "assistant",
                        "content": f"위스키 종류에는  {liquor_data_wisky}가 있습니다."}
                ]
            },
            {"messages": [
                {"role": "system", "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                {"role": "user", "content": "보드카로 만들 수 있는 칵테일은 무엇이 있나요?"},
                {"role": "assistant", "content": "'코스모폴리탄'을 추천드립니다. 보드카와 트리플 섹, 라임 주스, 크랜베리 주스를 섞어 새콤달콤한 맛을 내며, 도수가 높아 알코올 향도 느껴집니다."}
            ]
            },
            {
                "messages": [
                    {"role": "system", "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "새콤한 칵테일을 추천해 주세요."},
                    {"role": "assistant", "content": "'진 피즈'와 '블루 하와이'를 추천합니다. 두 칵테일 모두 새콤한 맛을 가지고 있는데, '진 피즈'는 진과 레몬즙, 탄산수가 주는 상큼하고 청량한 느낌이 강하고, '블루 하와이'는 파인애플 주스와 레몬즙이 들어가 과일향이 더 부드럽고 달콤합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "럼으로 만들 수 있는 칵테일은 무엇이 있나요?"},
                    {"role": "assistant", "content": "'블루 하와이'와 '준벅'을 추천합니다. 두 칵테일 모두 럼을 사용하며 달콤한 열대 과일 맛을 즐길 수 있지만, '블루 하와이'는 파인애플 주스가 강하게 들어가 과일향이 두드러지고, '준벅'은 미도리와 바나나 리큐르가 더 달콤한 맛을 줍니다."}
                ]},
            {
                "messages": [
                    {"role": "system", "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "도수가 높은 칵테일을 추천해 주세요."},
                    {"role": "assistant", "content": "'드라이 마티니'를 추천합니다. 진과 드라이 베르무트가 주재료이며, 깔끔하고 담백한 맛이 특징입니다. 알코올 도수가 높아 한 모금만 마셔도 강한 풍미를 느낄 수 있습니다."}
                ]},
            {

                "messages": [
                    {"role": "system", "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "단맛이 나는 칵테일을 추천해주세요."},
                    {"role": "assistant", "content": "'준벅'과 '동해'를 추천합니다. 두 칵테일 모두 과일 리큐르가 들어가 달콤한 맛이 강합니다. 그러나 '준벅'은 파인애플과 바나나의 달콤함이 주를 이루고, '동해'는 다양한 리큐르가 조화를 이루어 좀 더 복합적인 과일향을 즐길 수 있습니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "위스키를 베이스로 한 클래식 칵테일을 추천해 주세요."},
                    {"role": "assistant", "content": "'올드 패션드'와 '맨해튼'이 대표적인 위스키 기반 클래식 칵테일입니다. 두 칵테일 모두 위스키의 깊은 풍미를 잘 살리지만, '올드 패션드'는 설탕과 비터의 단맛과 쓴맛의 조화를 느낄 수 있고, '맨해튼'은 스위트 베르무트가 부드러운 질감을 더합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "열대 과일 맛이 나는 칵테일을 추천해 주세요."},
                    {"role": "assistant", "content": "'블루 하와이'와 '동해'를 추천합니다. 두 칵테일 모두 열대 과일 맛이 특징이며, '블루 하와이'는 파인애플 주스와 블루 큐라소의 상쾌한 과일향을 즐길 수 있고, '동해'는 복합적인 과일 리큐르가 주는 달콤함이 두드러집니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user",      "content": "그레이구스로 만들 수 있는 칵테일은 무엇인가요?"},
                    {"role": "assistant",
                        "content": "그레이구스 보드카로는 대표적으로 마티니를 만들 수 있습니다. 마티니는 보드카 또는 진을 기본으로 하며, 드라이 베르무트를 첨가하여 만드는 칵테일로, 강한 맛과 세련된 향이 특징입니다. 보통 올리브나 레몬 제스트로 장식하여 제공합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user",      "content": "보드카를 사용한 칵테일 중 단맛이 나는 칵테일 추천해주세요."},
                    {"role": "assistant",
                        "content": "'코스모폴리탄'을 추천드립니다. 보드카, 트리플 섹, 크랜베리 주스, 라임 주스를 섞어 만들며, 달콤하면서도 상큼한 맛이 특징인 칵테일입니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user",      "content": "깔끔한 보드카를 추천해 주세요."},
                    {"role": "assistant",
                        "content":  "추천할 만한 깔끔한 보드카로는 그레이구스(Gray Goose)와 스미노프(Smirnoff)가 있습니다. 그레이구스는 프리미엄 보드카로 부드러운 맛과 향이 특징이며, 스미노프는 가성비가 뛰어나면서도 깔끔한 맛을 제공합니다."}
                ]},
            {
                "messages": [
                    {"role": "system",
                        "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user",      "content": "스모키한 럼을 추천해 주세요."},
                    {"role": "assistant",
                        "content":  "추천할 만한 스모키한 럼으로는 더 크라켄(The Kraken)과 네그리타(Negra) 럼이 있습니다. 더 크라켄은 풍부한 향신료와 스모키한 맛이 특징이며, 네그리타는 부드러운 캐러멜 맛과 함께 스모키한 느낌을 줍니다."}
                ]},
            {
                "messages": [
                    {"role": "system",
                        "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "진으로 하이볼 말고 다른 걸 만들어먹을 순 없나요?"},
                    {"role": "assistant",
                        "content": "하이볼 외에 진을 즐기는 방법으로는 '스트레이트'나 '온더락'도 있고, 칵테일로는 '진 피즈'와 그린 올리브와 드라이베르무트를 추가한  '마티니'도 가능합니다."}
                ]
            },
            {
                "messages": [
                    {"role": "system",
                        "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "칵테일을 집에서 직접 만들어먹기 시작한지 얼마 안됐는데, 블루 큐라소로 블루 라군밖에 만들어먹지 못했습니다. 이걸로 만들 수 있는 다른 칵테일 레시피를 알려주세요. "},
                    {"role": "assistant",
                        "content": "웹사이트 내 레시피 중에는 '블루 하와이'가 있습니다. 또 일반적인 블루 라군에 토닉 워터를 넣어 롱드링크 버전으로 가볍게 즐길 수 있는 레시피도 있습니다. "}
                ]},
            {
                "messages": [
                    {"role": "system",
                        "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": "칵테일을 혼자 만들어먹어보고 싶은데, 평소 레몬, 오렌지 계열의 상큼한 맛을 좋아합니다.  리큐르와 칵테일 레시피 등 추천해주세요"},
                    {"role": "assistant",
                        "content": "상큼한 시트러스 계열의 리큐르로는 '디카이퍼 트리플 섹'과 '팔리니 리몬첼로'을 추천드립니다.  '디카이퍼 트리플 섹'으로 만든 추천 칵테일은 '마가리타'나 '코스모폴리탄'이 있으며,  '팔리니 리몬첼로' 로는 얼음을 가득 채운 잔에 부어 시원하게 음미하는 것도 좋고, '하이볼'도 추천드립니다."}
                ]},
            {
                "messages": [
                    {"role": "system",
                        "content": f"당신은 데이터 {liquor_data}와 {cocktail_data}안에서 사용자의 가진 술로 만들 수 있는 칵테일을 알려주는 어시스턴트입니다."},
                    {"role": "user", "content": " 텐커레이, 봄베이, 헨드릭스를 먹어봤는데, 안먹어본 새로운 진을 찾고있습니다. 너무 고가의 가격은 아니면서 평범한 맛이 아니었으면 좋겠어요."},
                    {"role": "assistant",
                        "content": " '재패니즈 진'인 '산토리 수이 진'을 추천합니다. 750ml에 5만원으로 , 다른 진에 비해 향히 상당히 강하고 특이한 편으로 스트레이트로 마셨을 때, 적당한 달달함과 솔방울과 같은 허브의 향이 입안 가득 퍼지고, 스파이시함으로 깔끔하게 마무리 되는 게 특징입니다."}
                ]},
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

        return Response({"message": "여까지 문제없음~"},status=status.HTTP_200_OK)
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
        return Response({f"message: {progress}"}, status=status.HTTP_201_CREATED)


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
        liquor_data1 = ""
        liquor_data2 = ""
        liquor_data3 = ""
        # 처음 질문을 받는 것이라면 system prompt에 사용자 정보를 넘겨줘야 하므로 데이터베이스 접근.
        if len(history) == 0:
            liquor_list = MyLiquor.objects.filter(
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
