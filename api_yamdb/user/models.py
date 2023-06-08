from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=50,
        default=USER,
        verbose_name='Роль',
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        verbose_name='Имя Пользователя'
    )
    email = models.EmailField(
        unique=True,
        null=False,
        verbose_name='Электронная почта'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username_not_me'
            )
        ]
