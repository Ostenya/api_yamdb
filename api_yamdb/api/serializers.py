from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title


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
