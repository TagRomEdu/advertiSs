from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users_app.apps import UsersAppConfig


app_name = UsersAppConfig.name

user_router = SimpleRouter()
user_router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('', include(user_router.urls)),
]
