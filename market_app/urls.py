from django.urls import include, path
from rest_framework.routers import DefaultRouter
from market_app.apps import MarketAppConfig
from market_app.views import AdvertisementViewSet


app_name = MarketAppConfig.name

ads_router = DefaultRouter()
ads_router.register(r'ads', AdvertisementViewSet, basename='ads')
reviews_router = DefaultRouter()
reviews_router.register(r'reviews', AdvertisementViewSet, basename='reviews')

urlpatterns = [
    path('', include(ads_router.urls)),
    path('', include(reviews_router.urls)),
]
