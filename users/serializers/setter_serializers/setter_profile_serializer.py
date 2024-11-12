from rest_framework import serializers

from users.models.setter import (
    Setter,
    SetterAwards,
    SetterCareer,
    SetterCertification,
    SetterEducation,
    SetterFreelancer,
)


class SetterCertificationSerializer(serializers.ModelSerializer):
    certification_uuid = serializers.UUIDField(read_only=True)
    proof_document = serializers.FileField(read_only=True)

    class Meta:
        model = SetterCertification
        fields = [
            "certification_uuid",
            "name",
            "issuing_authority",
            "proof_document",
        ]

    def create(self, validated_data):
        new_certification = SetterCertification.objects.create(
            setter=self.context.get("setter"), **validated_data
        )
        return new_certification

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class SetterAwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetterAwards
        fields = ["competition", "prize"]


class SetterCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetterCareer
        fields = ["company_name", "department", "period"]


class SetterFreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetterFreelancer
        fields = ["project_name", "description"]


class SetterEducationSerializer(serializers.ModelSerializer):
    education_uuid = serializers.UUIDField(read_only=True)
    proof_document = serializers.FileField(read_only=True)

    class Meta:
        model = SetterEducation
        fields = [
            "education_uuid",
            "school",
            "major",
            "academic_status",
            "proof_document",
        ]

    def create(self, validated_data):
        new_education = SetterEducation.objects.create(
            setter=self.context.get("setter"), **validated_data
        )
        return new_education

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class SetterProfileSerializer(serializers.Serializer):
    nickname = serializers.SerializerMethodField()
    education = SetterEducationSerializer(many=True, required=False)
    certification = SetterCertificationSerializer(many=True, required=False)
    awards = SetterAwardSerializer(many=True, required=False)
    career = SetterCareerSerializer(many=True, required=False)
    freelancer = SetterFreelancerSerializer(many=True, required=False)
    setter_link = serializers.CharField(required=True)
    setter_area = serializers.CharField(required=True)

    def get_nickname(self, obj):
        # Setter에서 user 객체에 존재하는 nickname 가져오기 위한 함수
        # SerializerMethodField가 사용한다.
        return obj.user.nickname

    def validate(self, attrs):
        # 1. 요청한 user가 이미 setter 프로필을 생성했는가?
        request = self.context.get("request")
        if Setter.objects.filter(user=request.user).exists():
            raise serializers.ValidationError(
                "해당 사용자는 이미 Setter 프로필을 등록하였습니다."
            )

        # 2. setter link가 http 또는 https로 시작하는가?
        if "setter_link" in attrs:
            if not (
                attrs["setter_link"].startswith("http://")
                or attrs["setter_link"].startswith("https://")
            ):
                raise serializers.ValidationError(
                    "Setter link는 http 또는 https로 시작해야 합니다."
                )

        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["education"] = SetterEducationSerializer(
            instance.setter_education.all(), many=True
        ).data
        representation["certification"] = SetterCertificationSerializer(
            instance.setter_certification.all(), many=True
        ).data
        representation["awards"] = SetterAwardSerializer(
            instance.setter_awards.all(), many=True
        ).data
        representation["career"] = SetterCareerSerializer(
            instance.setter_career.all(), many=True
        ).data
        representation["freelancer"] = SetterFreelancerSerializer(
            instance.setter_freelancer.all(), many=True
        ).data

        return representation

    def create(self, validated_data):
        user = self.context.get("request").user

        education_data = validated_data.pop("education", [])
        certification_data = validated_data.pop("certification", [])
        awards_data = validated_data.pop("awards", [])
        career_data = validated_data.pop("career", [])
        freelancer_data = validated_data.pop("freelancer", [])

        # 리포머 프로필 생성
        profile = Setter.objects.create(
            user=user,
            setter_area=validated_data["setter_area"],
            setter_link=validated_data["setter_link"],
        )

        # 중첩된 데이터 생성
        self.create_nested_data(
            profile=profile,
            education_data=education_data,
            certification_data=certification_data,
            awards_data=awards_data,
            career_data=career_data,
            freelancer_data=freelancer_data,
        )

        return profile

    def create_nested_data(
        self,
        profile,
        education_data,
        certification_data,
        awards_data,
        career_data,
        freelancer_data,
    ):

        for edu in education_data:
            SetterEducation.objects.create(setter=profile, **edu)

        for cert in certification_data:
            SetterCertification.objects.create(setter=profile, **cert)

        for award in awards_data:
            SetterAwards.objects.create(setter=profile, **award)

        for career in career_data:
            SetterCareer.objects.create(setter=profile, **career)

        for freelancer in freelancer_data:
            SetterFreelancer.objects.create(setter=profile, **freelancer)

    def update(self, instance, validated_data):
        education_data = validated_data.pop("education", [])
        certification_data = validated_data.pop("certification", [])
        awards_data = validated_data.pop("awards", [])
        career_data = validated_data.pop("career", [])
        freelancer_data = validated_data.pop("freelancer", [])

        # 기본 프로필 데이터 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 중첩된 데이터 업데이트 처리
        self.update_nested_data(
            profile=instance,
            education_data=education_data,
            certification_data=certification_data,
            awards_data=awards_data,
            career_data=career_data,
            freelancer_data=freelancer_data,
        )

        return instance

    def update_nested_data(
        self,
        profile,
        education_data,
        certification_data,
        awards_data,
        career_data,
        freelancer_data,
    ):

        SetterEducation.objects.filter(setter=profile).delete()
        for edu in education_data:
            SetterEducation.objects.create(setter=profile, **edu)

        SetterCertification.objects.filter(setter=profile).delete()
        for cert in certification_data:
            SetterCertification.objects.create(setter=profile, **cert)

        SetterAwards.objects.filter(setter=profile).delete()
        for award in awards_data:
            SetterAwards.objects.create(setter=profile, **award)

        SetterCareer.objects.filter(setter=profile).delete()
        for career in career_data:
            SetterCareer.objects.create(setter=profile, **career)

        SetterFreelancer.objects.filter(setter=profile).delete()
        for freelancer in freelancer_data:
            SetterFreelancer.objects.create(setter=profile, **freelancer)
