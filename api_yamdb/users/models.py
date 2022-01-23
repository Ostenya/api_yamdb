from django.contrib.auth.models import AbstractUser
<<<<<<< HEAD
from django.conf import settings
=======
from django.db import models

from api_yamdb.settings import (ADMINISTRATOR_ROLE, AUTHENTICATED_USER_ROLE,
                                MODERATOR_ROLE)
>>>>>>> 4f69946f9208ce4c9cb340499247b064efe83b79


class User(AbstractUser):
    ROLES = (
        (settings.AUTHENTICATED_USER_ROLE, 'Аутентифицированный пользователь'),
        (settings.MODERATOR_ROLE, 'Модератор'),
        (settings.ADMINISTRATOR_ROLE, 'Администратор'),
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
