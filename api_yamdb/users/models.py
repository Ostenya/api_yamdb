from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import (ADMINISTRATOR_ROLE, AUTHENTICATED_USER_ROLE,
                                MODERATOR_ROLE)


class User(AbstractUser):
    ROLES = (
        (AUTHENTICATED_USER_ROLE, 'Аутентифицированный пользователь'),
        (MODERATOR_ROLE, 'Модератор'),
        (ADMINISTRATOR_ROLE, 'Администратор'),
    )
    email = models.EmailField(
        verbose_name='Электронный адрес',
        blank=False,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=10,
        choices=ROLES,
        default='user',
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super(User, self).save(*args, **kwargs)
