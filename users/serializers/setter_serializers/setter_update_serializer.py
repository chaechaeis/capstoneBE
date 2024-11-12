from rest_framework import serializers

from users.models.setter import Setter


class SetterUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Setter
        fields = ["setter_link", "setter_area"]
        extra_kwargs = {
            "setter_link": {"required": False},
            "setter_area": {"required": False},
        }

    def validate(self, attrs):
        if (
            "setter_link" in attrs
            and attrs["setter_link"] == self.instance.setter_link
        ):
            raise serializers.ValidationError("setter_link must be different")

        if (
            "setter_area" in attrs
            and attrs["setter_area"] == self.instance.setter_area
        ):
            raise serializers.ValidationError("setter_area must be different")

        return attrs

    def update(self, instance, validated_data):
        instance.setter_link = validated_data.get(
            "setter_link", instance.setter_link
        )
        instance.setter_area = validated_data.get(
            "setter_area", instance.setter_area
        )
        instance.save()
        return instance
