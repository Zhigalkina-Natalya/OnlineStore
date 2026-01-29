from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Используем email как поле для авторизации (USERNAME_FIELD).
    Дополнительные поля: avatar, phone, country.
    """

    username = None

    # email — уникален и служит для аутентификации
    email = models.EmailField(unique=True, verbose_name="Email")

    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True, help_text="Загрузите свой аватар"
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", blank=True, null=True, help_text="Введите номер телефона"
    )
    country = models.CharField(max_length=100, blank=True)

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
