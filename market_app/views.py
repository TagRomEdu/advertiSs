from django.shortcuts import render
from rest_framework import viewsets
from market_app.models import Advertisement, Review
from market_app.paginators import AdvertisementPaginator

from market_app.serializers import AdvertisementSerializer, ReviewSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    pagination_class = AdvertisementPaginator


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
