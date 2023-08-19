import re

from django.conf import settings
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import User


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region=settings.PHONE_NUMBER_REGION)


class TokenCreateSerializer(PhoneNumberSerializer):
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        required=True,
    )

class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(
        required=True,
    )


    def validate_invite_code(self, value):
        if not re.match(r"^[a-zA-Z0-9]{6}$", value):
            raise serializers.ValidationError(
                "Некорректный инвайт код",
            )
        return super().validate(value)


class UserSerializer(serializers.ModelSerializer):
    invitings = serializers.StringRelatedField(
        many=True,
    )
    invited_by_code = serializers.ReadOnlyField(
        source="inviter.invite_code",
    )

    class Meta:
        model = User
        fields = (
            "phone_number",
            "username",
            "email",
            "first_name",
            "last_name",
            "invite_code",
            "invited_by_code",
            "invitings",
        )
        read_only_fields = (
            "invite_code",
            "invited_by_code",
            "invitings",
        )
