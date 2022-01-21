from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, exceptions
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import PasswordField
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year',
                  'rating', 'description',
                  'genre', 'category')
        read_only_fields = ('id', 'rating')
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class TitlePostSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(many=True, queryset=Genre.objects.all(),
                             slug_field='slug')

    category = SlugRelatedField(queryset=Category.objects.all(),
                                slug_field='slug')

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')
        model = Title
        validators = [UniqueTogetherValidator(
            queryset=Title.objects.all(),
            fields=('name', 'category')
        )]

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'Проверьте год выпуска произведения! '
                'Он не может быть больше текущего года')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True,
                              default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author',
                  'score', 'pub_date')
        model = Review
        read_only_fields = ('author',)
        # validators = [UniqueTogetherValidator(
        #     queryset=Review.objects.all(),
        #     fields=('title', 'author')
        # )]


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


class UserSelfSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('username', 'email', 'role',)


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Укажите username, отличный от me')
        return value


class MyTokenObtainSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = PasswordField()

    def validate(self, attrs):
        self.user = get_object_or_404(
            User,
            username=attrs[self.username_field]
        )
        if self.user is None or not self.user.is_active:
            raise exceptions.ValidationError('Несуществующий пользователь')
        if not default_token_generator.check_token(
            self.user,
            attrs['confirmation_code']
        ):
            raise exceptions.ValidationError('Невалидный код подтверждения')
        return {'access_token': str(AccessToken.for_user(self.user))}
