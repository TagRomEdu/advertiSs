from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from market_app.models import Advertisement, Review
from market_app.paginators import AdvertisementPaginator, ReviewPaginator
from market_app.permissions import IsAuthorOrAdmin
from market_app.serializers import (AdvertisementSerializer,
                                    MyAdsSerializer, ReviewSerializer)


class AdvertisementViewSet(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    pagination_class = AdvertisementPaginator
    permission_classes_by_action = {'list': [AllowAny],
                                    'partial_update': [IsAuthorOrAdmin],
                                    'update': [IsAuthorOrAdmin],
                                    'destroy': [IsAuthorOrAdmin],
                                    }

    def get_permissions(self):
        return [permission() for permission in
                self.permission_classes_by_action.get(self.action,
                                                      [IsAuthenticated])
                ]


class AdsListAPIView(generics.ListAPIView):
    serializer_class = MyAdsSerializer
    queryset = Advertisement.objects.all()
    pagination_class = AdvertisementPaginator
    permission_classes = [IsAuthorOrAdmin]

    def get_queryset(self):
        return Advertisement.objects.filter(author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = ReviewPaginator
    permission_classes_by_action = {'list': [AllowAny],
                                    'partial_update': [IsAuthorOrAdmin],
                                    'update': [IsAuthorOrAdmin],
                                    'destroy': [IsAuthorOrAdmin],
                                    }

    def get_permissions(self):
        return [permission() for permission in
                self.permission_classes_by_action.get(self.action)]
