from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, SignUpView,
                       UserViewSet, UserSelfView,)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='v1_categories')
router_v1.register('genres', GenreViewSet, basename='v1_genres')
router_v1.register('titles', TitleViewSet, basename='v1_titles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='v1_reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='v1_comments'
)
router_v1.register('users', UserViewSet, basename='v1_users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/signup/',
        SignUpView.as_view(),
        name='sign_up'
    ),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('v1/users/me', UserSelfView.as_view()),
]
