from django.urls import include, path
from rest_framework.routers import DefaultRouter
from market_app.apps import MarketAppConfig
from market_app.views import (AdsListAPIView, AdvertisementViewSet,
                              ReviewViewSet)


app_name = MarketAppConfig.name

router = DefaultRouter()
router.register(r'ads', AdvertisementViewSet, basename='ads')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('advs/me/', AdsListAPIView.as_view(), name='my_ads')
]
