from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter


from users_app.apps import UsersAppConfig


app_name = UsersAppConfig.name

user_router = SimpleRouter()
user_router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('', include(user_router.urls)),
    path('', include('djoser.urls.jwt')),
]
