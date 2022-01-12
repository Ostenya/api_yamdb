from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name='имя')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='техническое имя')
    description = models.TextField(blank=True, verbose_name='описание')

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name='имя')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='техническое имя')
    description = models.TextField(blank=True, verbose_name='описание')

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(Genre,
                                   through='TitleGenre',
                                   verbose_name='жанр')
    category = models.ForeignKey(Category,
                                 to_field='slug',
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 related_name='title',
                                 verbose_name='категория'
                                 )

    class Meta:
        verbose_name = "произведение"
        verbose_name_plural = "произведения"
        ordering = ('name', 'category')
        constraints = [models.UniqueConstraint(
            fields=['name', 'category'],
            name='unique_name_category',
        )]

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "произведение - жанр"
        verbose_name_plural = "произведения - жанры"
        constraints = [models.UniqueConstraint(
            fields=['title', 'genre'],
            name='unique_title_genre',
        )]

    def __str__(self):
        return f'{self.title.name} - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='автор'
    )
    text = models.TextField(verbose_name='текст')
    score = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 11)],
        verbose_name='оценка'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='дата создания отзыва')

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        ordering = ('-pub_date',)
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique_title_author',
        )]

    def __str__(self):
        return f'{self.title} - {self.author.username}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='произведение, к которому добавлен комментарий'
    )
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='дата создания')

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
        ordering = ('-pub_date',)

    def __str__(self):
        return (f'{self.review.title} - {self.author.username} - '
                f'{self.text[:15]}')
