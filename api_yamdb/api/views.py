from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, permissions, viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from rest_framework.pagination import PageNumberPagination

from api.permissions import (AdminOnly, AdminOrReadOnly,
                             ModeratorAdminAuthorOrReadOnly,)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer, UserSerializer,
                             UserSelfSerializer, SignUpSerializer,
                             MyTokenObtainSerializer,)
from reviews.models import Category, Genre, Title
from users.models import User


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ModeratorAdminAuthorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination


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
            s_user.extendeduser.confirmation_code = confirmation_code
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


class UserSelfView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSelfSerializer

    def get_object(self):
        obj = get_object_or_404(User, username=self.request.user.username)
        self.check_object_permissions(self.request, obj)
        return obj


class UserSelfView2(APIView):
    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSelfSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSelfSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainView(TokenViewBase):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainSerializer
