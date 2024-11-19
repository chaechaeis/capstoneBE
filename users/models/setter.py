import uuid

from django.db import models

from core.models import TimeStampedModel
from users.models.user import User



class Setter(models.Model):
    # 세터 기본 프로필 정보
    # 닉네임, 소개글은 User 테이블에 있는 필드 사용 -> 세터 생성 요청 시 필요
    # 추후 스타일 선택을 위해서 seeker와 setter의 model 분류함
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="setter_profile"
    )
    class Meta:
        db_table = "setter_profile"



