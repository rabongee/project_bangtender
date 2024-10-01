from django.core.exceptions import ValidationError
from .models import Cocktail


# 작성중...
# 등록 > 각각 요소 입력 확인, 중복 확인,
# 수정 > 빈 요소가 없는지 확인, 중복 ,
# 삭제 > 

# 칵테일 이름의 중복을 확인하는 함수
def validate_unique_cocktail_name(name):
    err_msg = []

    if (name := name.get("name")):
        if Cocktail.objects.filter(name=name).exists():
            err_msg.append({"name": "이미 등록된 칵테일 이름입니다."})