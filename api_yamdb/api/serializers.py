from django.db.models import Avg
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from rest_framework import exceptions, serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import (TokenObtainSerializer,
                                                  PasswordField)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year',
                  'rating', 'description',
                  'genre', 'category')
        model = Title
        validators = [UniqueTogetherValidator(
            queryset=Title.objects.all(),
            fields=('name', 'category')
        )]

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'Проверьте год выпуска произведения! '
                'Он не может быть больше текущего года')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author',
                  'score', 'pub_date')
        model = Review
        validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=('name', 'author')
        )]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
        extra_kwargs = {'username': {'required': True,
                                     'allow_blank': False},
                        'email': {'required': True,
                                  'allow_blank': False}}

    def validate_username(self, value):
        if (
            User.objects.filter(username=value).exists()
            or value == 'me'
        ):
            raise serializers.ValidationError(
                'Укажите непустой уникальный username, отличный от me')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Нужен уникальный email')
        return value


class MyTokenObtainSerializer(TokenObtainSerializer):
    confirmation_code = PasswordField()

    def validate(self, attrs):
        if not default_token_generator.check_token(
            self.user,
            attrs['confirmation_code']
        ):
            raise exceptions.AuthenticationFailed(
                f'Некорректный код подтверждения {attrs['confirmation_code']},
            )
        if (
            not User.objects.filter(username=self.user.username).exists()
            or not self.user.is_active
        ):
            raise exceptions.AuthenticationFailed(
                f'Активный пользователь с таким именем {self.user} не найден'
            )
        return {}
