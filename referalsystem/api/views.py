import secrets
import time

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from api.serializers import (
    InviteCodeSerializer,
    PhoneNumberSerializer,
    TokenCreateSerializer,
    UserSerializer,
)


class SignUpView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        user, _ = User.objects.get_or_create(
            phone_number=phone_number,
        )
        user.confirmation_code = "".join(
            secrets.choice(settings.CONFIRMATION_CODE_CHARS)
                for _ in range(settings.CONFIRMATION_CODE_LENGTH)
        )
        user.save(update_fields=["confirmation_code"])

        # Иммитация отправки кода подтверждения
        time.sleep(1)

        return Response(serializer.data)

class TokenView(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data["confirmation_code"]
        phone_number = serializer.validated_data["phone_number"]
        user = get_object_or_404(User, phone_number=phone_number)

        if (
            user.confirmation_code == settings.INTRUDER_STOPPER
        ):
            return Response(
                {"message": "Код подтверждения недействителен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (user.confirmation_code != confirmation_code):
            user.confirmation_code = settings.INTRUDER_STOPPER
            user.save(update_fields=["confirmation_code"])
            return Response(
                {"message": "Неверный код подтверждения"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.confirmation_code = settings.INTRUDER_STOPPER
        user.save(update_fields=["confirmation_code"])
        token = AccessToken.for_user(user)
        return Response({"Bearer": f"{token}"})


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "phone_number"

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        current_user = request.user

        if request.method == "GET":
            return Response(self.get_serializer(current_user).data)

        serializer = self.get_serializer(
            current_user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(IsAuthenticated,),
    )
    def activate_invite_code(self, request):
        current_user = request.user

        if current_user.inviter:
            return Response(
                {"message": "Инвайт код уже активирован"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = InviteCodeSerializer(
            current_user,
            request.data,
        )
        serializer.is_valid(raise_exception=True)
        invite_code = serializer.validated_data.get("invite_code")

        if current_user.invite_code == invite_code:
            return Response(
                {"message": "Недопустимо использовать собственный инвайт код"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            current_user.inviter = User.objects.get(invite_code=invite_code)
            current_user.save()
            return Response(
                    serializer.data,
                )

        except User.DoesNotExist:
            return Response(
                    {"message": "Предоставленный код не действителен"},
                    status=status.HTTP_404_NOT_FOUND,
                )
