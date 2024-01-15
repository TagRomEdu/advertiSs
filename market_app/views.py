from rest_framework import viewsets, generics
from market_app.models import Advertisement, Review
from market_app.paginators import AdvertisementPaginator

from market_app.serializers import (AdvertisementSerializer,
                                    MyAdsSerializer, ReviewSerializer)


class AdvertisementViewSet(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    pagination_class = AdvertisementPaginator


class AdsListAPIView(generics.ListAPIView):
    serializer_class = MyAdsSerializer
    queryset = Advertisement.objects.all()

    def get_queryset(self):
        return Advertisement.objects.filter(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
