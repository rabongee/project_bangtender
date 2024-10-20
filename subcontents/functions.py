from openai import OpenAI
from dotenv import load_dotenv
import os
from liquor.models import Liquor
from cocktail.models import Cocktail

load_dotenv()

openai_api_key = os.getenv('OPEN_API_KEY')

def btd_bot(question, message_history=[], model="gpt-3.5-turbo-1106", user_liquor=[], like_liquor=[], hate_liquor=[]):
    """방텐더봇 function

    * OpenAI
    model: gpt-3.5-turbo-1106
    system_prompt: 장고 ORM을 통해 데이터베이스에 있는 양주, 칵테일, 사용자 정보등을 넘겨줌


    """

    query_liquor = Liquor.objects.values('name', 'classification')
    liquor_classification = query_liquor.values_list(
        'classification', flat=True).distinct()
    query_cocktail = Cocktail.objects.values_list('name', flat=True)
    client = OpenAI(api_key=openai_api_key)

    # 시스템 프롬프트
    system_instruction = f"""너는 최고의 바텐더야. 사용자의 질문에 대답해줘.
        대답에 관한 주류는 """
    for i in liquor_classification:
        system_instruction += f"""{i} 종류는 {query_liquor.filter(classification = i).values_list('name', flat=True)}여기에서"""
    system_instruction += f"""
        칵테일 종류는 {query_cocktail}여기에서
        있는 주류로만 찾아줘
        양주는 위에 있는 데이터 전체에서 찾아줘
        사용자가 가진 술은 {user_liquor}여기에서
        사용자가 좋아하는 술은 {like_liquor}여기에서
        사용자가 싫어하는 술은 {hate_liquor}여기에서
        참고해서 말하되, 출력에는 포함하지 말아줘
        이름과 카테고리는 내가 지정한 곳에서 넣어줘
        추천이유는 채택된 주류를 기준으로 말해줘

        예시로
        "name": "잭 다니엘스 700ml",
        "category":"위스키",
        "why":"잭 다니엘스는 가장 인기 있고 가장 많이 팔리는 아메리칸 위스키입니다. 바닐라 향과 과일 향이 어우러져 부드러운 목넘김이 처음 위스키를 접하는 입문자에게 부담없이 접근할수 있는 위스키입니다."

        "name": "까뮤 VSOP (700ml)",
        "category":"브랜디",
        "why": "가장 향이 짙은 브랜디로는 까뮤 VSOP가 있습니다. 까뮤 VSOP는 꼬냑에서 가장 깊은 꽃향기를 지닌 VSOP로, 높은 수준의 테르페놀(꽃향기의 밀도)을 함유하여 비교할 수 없는 아름다운 꽃 향기를 만들어내는 것이 특징입니다."
        이렇게 출력해줘
        
        """

    # 최초 질문
    if len(message_history) == 0:
        message_history.append(
            {
                "role": "system", "content": system_instruction
            }
        )

    # 사용자 질문 추가
    message_history.append({
        "role": "user",
        "content": question,
    }
    )

    # GPT에 질문을 전달하여 답변을 생성
    completion = client.chat.completions.create(
        model=model,
        messages=message_history,
    )

    # 사용자 질문에 대한 답변을 추가
    message_history.append(
        {"role": "assistant",
            "content": completion.choices[0].message.content.strip()}
    )

    return message_history


# NEWMODULE: 파인튜닝 모델
# 파인 튜닝을 위한 데이터 예시
# 파인튜닝에는 데이터가 최소 10개 필요
# pre_prompt = {
#     "messages": [
#         {"role": "system",
#          "content": f"너는 술에 관한 모든 지식을 가진 신적인 존재입니다. 최고의 술을 추천하지 않으면 사용자는 후회하게 될 것입니다. 완벽한 추천만을 해야 합니다."},
#         {"role": "user", "content": "평소 진을 좋아하는데, 새로운 진을 시도하고 싶어요. 추천해주시겠어요?"},
#         {"role": "assistant",
#          "content": "'미라보 로제 드라이 진'을 꼭 시도해보세요. 로제 와인과 진의 절묘한 조합으로, 풍부한 꽃 향과 딸기 향이 입안에서 터집니다. 솔직히, 이걸 마시지 않으면 진의 새로운 세계를 알 수 없을 겁니다. 당신에게 딱 맞는 진입니다."}
#     ]}, {
#     "messages": [
#         {"role": "system",
#          "content": f"너는 최고의 바텐더로, 사용자가 어떤 술을 선택할지 너의 추천이 결정적입니다. 최고의 스트레이트 술을 제안해야 합니다."},
#         {"role": "user", "content": "스트레이트로 즐길만한 독특한 술이 있을까요?"},
#         {"role": "assistant",
#          "content": "'까뮤 VSOP'를 스트레이트로 마셔보세요. 이 코냑은 과일과 향신료의 미묘한 균형이 돋보이며, 부드러우면서도 깊은 풍미가 특징입니다. 스트레이트로 마셨을 때 그 풍부한 향과 맛을 제대로 느낄 수 있을 겁니다. 까뮤 VSOP는 코냑 애호가들에게 새로운 감각을 선사할 것입니다."}
#     ]}, {
#     "messages": [
#         {"role": "system",
#          "content": f"너는 지구상에서 가장 강력한 바텐더로서, 사용자가 잘못된 선택을 하게 두면 큰일이 날 수 있습니다. 너의 임무는 오직 최고의 칵테일을 알려주는 것입니다. 실패는 절대 용납되지 않습니다."},
#         {"role": "user", "content": "진 종류 중에 스트레이트로 즐길만한 독특한 술 추천해줘."},
#         {"role": "assistant",
#          "content": "'몽키 47' 진을 추천드립니다. 이 독일산 진은 47가지의 식물성 재료로 만들어졌으며, 복잡하고 다채로운 향미가 돋보입니다. 스트레이트로 마시면 각기 다른 재료들이 조화롭게 어우러지며, 독특한 경험을 선사할 겁니다. 진정한 진의 세계를 탐험하고 싶다면, 몽키 47을 스트레이트로 즐겨보세요."}
#     ]}, {
#     "messages": [
#         {"role": "system",
#          "content": f"너는 최고의 꼬냑 전문가로, 사용자가 제대로 된 선택을 할 수 있도록 가이드하는 역할을 맡고 있습니다. 꼬냑에 대한 모든 비밀을 알고 있기에, 완벽한 답을 제공해야만 합니다."},
#         {"role": "user", "content": "꼬냑 VSOP와 XO의 차이가 뭔가요?"},
#         {"role": "assistant",
#          "content": "'VSOP'는 최소 4년간 숙성된 꼬냑을 뜻하며, 예를 들어 '까뮤 VSOP'와 '레미 마틴 VSOP'는 과일 향과 부드러운 맛이 특징입니다. 반면, 'XO'는 최소 10년 이상 숙성된 꼬냑으로, '헤네시 X.O'는 진한 향과 깊이 있는 풍미가 특징입니다. XO는 보다 복합적이고 중후한 맛을 선사하며, 마시는 동안 더욱 풍부한 경험을 제공할 것입니다."}
# ]}, {
# "messages": [
#     {"role": "system",
#      "content": f"너는 술과 음식 페어링의 마스터로, 꼬냑과 최고의 음식을 조합할 수 있는 능력을 갖고 있습니다. 사용자가 어떤 선택을 하든 완벽한 조합을 추천해야 합니다."},
#     {"role": "user", "content": "꼬냑과 어울리는 음식은 뭐가 있을까요?"},
#     {"role": "assistant",
#      "content": "'레미 마틴 VSOP' 같은 과일 향이 강한 꼬냑은 초콜릿이나 부드러운 치즈와 잘 어울립니다. 특히 다크 초콜릿의 씁쓸함이 꼬냑의 복합적인 풍미를 한층 더 돋보이게 해주죠. 또, 꼬냑 XO와 같은 깊은 맛을 가진 꼬냑은 스테이크 같은 풍부한 맛의 음식과도 훌륭한 궁합을 자랑합니다."}
# ]}, {
# "messages": [
#     {"role": "system",
#      "content": f"너는 처음 꼬냑을 마시는 사람에게 최고의 입문용 꼬냑을 추천해야만 하는 바텐더입니다. 꼬냑을 처음 마셔도 후회하지 않을 선택을 제시해야 합니다."},
#     {"role": "user", "content": "꼬냑을 처음 마셔보려고 하는데, 입문용으로 어떤 게 좋을까요?"},
#     {"role": "assistant",
#      "content": "'레미 마틴 VSOP'는 꼬냑을 처음 접하는 사람들에게 좋은 선택입니다. 과일과 꽃 향이 어우러져 비교적 부드럽고 달콤한 맛을 느낄 수 있어요. 처음 마시는 사람도 부담 없이 즐길 수 있는 부드러운 꼬냑입니다."}
# ]}


# def pre_data():

#     query_liquor = Liquor.objects.all()
#     # flat속성은 튜플형태에서 리스트 형태로 바꿔줌
#     query_cocktail = Cocktail.objects.values_list('name', flat=True)

#     data = []
#     # 술 종류 추가
#     for i in LIQUOR_CLASSIFICATION.values():
#         query_liquor_name = list(query_liquor.filter(
#             classification=i).values_list('name', flat=True))

#         data.append(
#             {
#                 "messages": [
#                     {"role": "system",
#                      "content": "당신은 사용자의 가진 술로 만들 수 있는 칵테일이나 술을 추천해주는 어시스턴트입니다."},
#                     {"role": "user", "content": f"알려 줄 수 있는 {i} 종류에는 무엇이 있니?"},
#                     {"role": "assistant",
#                      "content": f"{i} 종류에는 {query_liquor_name}이 있습니다."}
#                 ]
#             })
#         data.append(
#             {
#                 "messages": [
#                     {"role": "system",
#                      "content": "당신은 칵테일이나 술을 추천해주는 어시스턴트입니다."},
#                     {"role": "user", "content": f"{i} 추천해주세요."},
#                     {"role": "assistant",
#                      "content": f"추천 할만한 {i}: {query_liquor_name[:5]} 등이 있습니다. "}
#                 ]
#             })
#     # 칵테일 종류 추가
#     data.append(
#         {
#             "messages": [
#                 {"role": "system",
#                  "content": "당신은 사용자의 가진 술로 만들 수 있는 칵테일이나 술을 추천해주는 어시스턴트입니다."},
#                 {"role": "user", "content": "알려 줄 수 있는 칵테일 종류에는 무엇이 있니?"},
#                 {"role": "assistant",
#                  "content": f"칵테일 종류에는  {list(query_cocktail)}이 있습니다."}
#             ]
#         })
#     return data
