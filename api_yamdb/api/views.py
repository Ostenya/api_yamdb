from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions, viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer, UserSerializer,
                             UserSelfSerializer,)
from reviews.models import Category, Genre, Review, Title
from users.models import User
from api.permissions import ModeratorAuthorOrReadOnly, AdminOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Review, pk=title_id)
        review = get_object_or_404(title, pk=review_id)
        return review.comments.all()


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSelfSerializer(data=request.data)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
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
