import uuid

from django.db import models

from core.models import TimeStampedModel
from users.models.user import User


def get_setter_certification_upload_path(instance, filename):
    email_name = instance.setter.user.email.split("@")[0]
    return f"users/{email_name}/setter/certifications/{filename}"


def get_portfolio_upload_path(instance, filename):
    email_name = instance.setter.user.email.split("@")[0]
    return f"users/{email_name}/setter/portfolio/{filename}"


class Setter(models.Model):
    # 세터 기본 프로필 정보
    # 닉네임, 소개글은 User 테이블에 있는 필드 사용 -> 세터 생성 요청 시 필요
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="setter_profile"
    )

    class Meta:
        db_table = "setter_profile"


class SetterEducation(models.Model):
    # 리포머 학력
    setter = models.ForeignKey(
        "users.Setter", on_delete=models.CASCADE, related_name="setter_education"
    )
    education_uuid = models.UUIDField(
        primary_key=True, null=False, unique=True, default=uuid.uuid4
    )
    school = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    academic_status = models.CharField(max_length=100)
    proof_document = models.FileField(
        upload_to=get_setter_certification_upload_path, null=True, blank=True
    )  # S3에 저장되는 경로

    class Meta:
        db_table = "setter_education"


class SetterCertification(models.Model):
    # 리포머 자격증 내역
    setter = models.ForeignKey(
        "users.Setter",
        on_delete=models.CASCADE,
        related_name="setter_certification",
    )
    certification_uuid = models.UUIDField(
        primary_key=True, null=False, unique=True, default=uuid.uuid4
    )
    name = models.CharField(max_length=100)  # 자격증 명
    issuing_authority = models.CharField(max_length=100)  # 자격증 발급기관 명
    proof_document = models.FileField(
        upload_to=get_setter_certification_upload_path, null=True, blank=True
    )

    class Meta:
        db_table = "setter_certification"


class SetterAwards(models.Model):
    # 리포머 수상 내역
    setter = models.ForeignKey(
        "users.Setter", on_delete=models.CASCADE, related_name="setter_awards"
    )
    award_uuid = models.UUIDField(
        primary_key=True, null=False, unique=True, default=uuid.uuid4
    )
    competition = models.CharField(max_length=100)  # 공모전 명
    prize = models.CharField(max_length=100)  # 수상 명
    proof_document = models.FileField(
        upload_to=get_setter_certification_upload_path, null=True, blank=True
    )

    class Meta:
        db_table = "setter_awards"


class SetterCareer(models.Model):
    # 리포머 경력
    setter = models.ForeignKey(
        "users.Setter", on_delete=models.CASCADE, related_name="setter_career"
    )
    career_uuid = models.UUIDField(
        primary_key=True, null=False, unique=True, default=uuid.uuid4
    )
    company_name = models.CharField(max_length=100)  # 근무 회사
    department = models.CharField(max_length=100, null=True, blank=True)  # 근무 부서
    period = models.CharField(
        max_length=30
    )  # 경력 기간 (O년, O개월, .. 이런식으로 입력한다고 하네요)
    proof_document = models.FileField(
        upload_to=get_setter_certification_upload_path, null=True, blank=True
    )

    class Meta:
        db_table = "setter_career"


class SetterFreelancer(models.Model):
    # 리포머 프리랜서/외주 경력
    setter = models.ForeignKey(
        "users.Setter", on_delete=models.CASCADE, related_name="setter_freelancer"
    )
    freelancer_uuid = models.UUIDField(
        primary_key=True, null=False, unique=True, default=uuid.uuid4
    )
    project_name = models.CharField(max_length=100)  # 프로젝트 이름
    description = (
        models.TextField()
    )  # 프리랜서/외주 수행 시 어떤 일을 했는지에 대한 설명을 저장하는 필드
    proof_document = models.FileField(
        upload_to=get_setter_certification_upload_path, null=True, blank=True
    )

    class Meta:
        db_table = "setter_freelancer"
