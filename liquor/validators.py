from decimal import Decimal, InvalidOperation
from .models import Liquor

def validator_liquor(data, liquor_instance=None):
    required_fields = ["name", "classification", "img", "content", "taste", "abv", "price"]

    # 필수 필드 검증
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field} 필드를 입력해 주세요."

    # abv(알코올 도수) 검증 로직
    abv = data.get("abv")
    try:
        # Decimal 변환 및 소수점 자리수 제한
        abv = Decimal(abv)
        if abv.as_tuple().exponent < -1:
            return False, "abv(알코올 도수)는 소수점 이하 1자리까지만 허용됩니다."
    except InvalidOperation:
        return False, "abv(알코올 도수)는 숫자여야 합니다."

    if not (0 <= abv < 100):
        return False, "abv(알코올 도수)는 0에서 100 사이의 값이어야 합니다."

    # 가격(price) 검증 로직
    price = data.get("price")
    try:
        price = int(price)  # 정수로 변환
        if price <= 0:
            return False, "price는 양의 정수여야 합니다."
    except (ValueError, TypeError):
        return False, "price는 양의 정수여야 합니다."

    # 이름 중복 방지 (수정 시 해당 객체 제외)
    name = data.get("name")
    if name:
        if liquor_instance:
            # 수정하는 경우, 현재 주류를 제외하고 중복 확인
            if Liquor.objects.exclude(id=liquor_instance.id).filter(name=name).exists():
                return False, "이미 존재하는 주류 이름입니다."
        else:
            # 새로 추가하는 경우 중복 확인
            if Liquor.objects.filter(name=name).exists():
                return False, "이미 존재하는 주류 이름입니다."

    return True, None