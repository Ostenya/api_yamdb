from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
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


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.TextField(
        'Код подтверждения',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Дополнительные параметры пользователя'

    def __str__(self):
        return self.confirmation_code


@receiver(post_save, sender=User)
def create_or_update_user_ExtendedUser(sender, instance, created, **kwargs):
    if created:
        ExtendedUser.objects.create(
            user=instance,
        )
        instance.extendeduser.save()
