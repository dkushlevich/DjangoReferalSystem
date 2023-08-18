import secrets

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Кастомная модель пользователя"""

    phone_number = PhoneNumberField(
        verbose_name="Номер телефона",
        region=settings.PHONE_NUMBER_REGION,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=settings.MAX_LENGTH_FIRST_NAME,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=settings.MAX_LENGTH_LAST_NAME,
        blank=True,
    )
    username = models.CharField(
        ("Ник пользователя"),
        max_length=150,
        blank=True,
        null=True,
        validators=[UnicodeUsernameValidator()],
        unique=True,
    )
    confirmation_code = models.CharField(
        verbose_name="Код авторизации",
        blank=True,
        null=True,
        max_length=settings.CONFIRMATION_CODE_LENGTH,
    )
    invite_code = models.CharField(
        verbose_name="Инвайт-код",
        blank=True,
        null=True,
        max_length=settings.INVITE_CODE_LENGTH,
        editable=False,
    )
    inviter = models.ForeignKey(
        "self",
        related_name="invitings",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


    def __str__(self) -> str:
        return str(self.phone_number)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invite_code = "".join(
                secrets.choice(settings.INVITE_CODE_CHARS)
                for _ in range(settings.INVITE_CODE_LENGTH)
            )
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.inviter == self:
            raise ValidationError(
                {"inviter": "Приглашение самого себя запрещено"},
            )
        return super().clean()
