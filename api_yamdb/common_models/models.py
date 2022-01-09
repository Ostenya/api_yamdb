from django.db import models


class Categories(models.Model):
    CHOICES = (
        ('film', 'Фильмы'),
        ('book', 'Книги'),
        ('music', 'Музыка'),
    )
    name = models.CharField(max_length=5, choices = CHOICES, verbose_name='название категории')

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name
