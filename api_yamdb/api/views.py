from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from api.filters import TitleFilter
from api.permissions import (AdminOnly, AdminOrReadOnly,
                             ModeratorAdminAuthorOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, MyTokenObtainSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitlePostSerializer, TitleSerializer,
                             UserSelfSerializer, UserSerializer)
from reviews.models import Category, Genre, Title
from users.models import User


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug',)

    def retrieve(self, request, slug=None):
        if not Category.objects.filter(slug=slug).exists():
            return Response(f'Категория {slug} отсутствует',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        slug = kwargs['slug']
        if not Category.objects.filter(slug=slug).exists():
            return Response(f'Категория {slug} отсутствует',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance,
                                             data=request.data,
                                             partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug',)

    def retrieve(self, request, slug=None):
        if not Genre.objects.filter(slug=slug).exists():
            return Response(f'Жанр {slug} отсутствует',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        slug = kwargs['slug']
        if not Genre.objects.filter(slug=slug).exists():
            return Response(f'Категория {slug} отсутствует',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance,
                                             data=request.data,
                                             partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (ModeratorAdminAuthorOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user,
                        title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializer
        else:
            return TitlePostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ModeratorAdminAuthorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(title.reviews.all(), pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            s_user = get_object_or_404(
                User,
                username=serializer.data['username']
            )
            confirmation_code = default_token_generator.make_token(s_user)
            send_mail(
                'Код потверждения',
                f'Ваш код подтверждения: {confirmation_code}',
                'from@api_yamdb.ru',
                [serializer.data['email']],
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me_get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = UserSelfSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSelfSerializer(
            user,
            data=request.data,
            many=False,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainView(TokenViewBase):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainSerializer
