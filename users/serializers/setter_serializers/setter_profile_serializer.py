from rest_framework import serializers

from users.models.setter import (
    Setter
)



class SetterProfileSerializer(serializers.Serializer):
    nickname = serializers.SerializerMethodField()

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

        return attrs

    def create(self, validated_data):
        user = self.context.get("request").user

        # setter 프로필 생성
        profile = Setter.objects.create(
            user=user,

        )

        # 중첩된 데이터 생성
        self.create_nested_data(
            profile=profile,
        )

        return profile


    def update(self, instance, validated_data):

        # 기본 프로필 데이터 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 중첩된 데이터 업데이트 처리
        self.update_nested_data(
            profile=instance,
        )

        return instance

