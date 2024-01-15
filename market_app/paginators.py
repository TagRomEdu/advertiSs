from rest_framework.pagination import PageNumberPagination


class AdvertisementPaginator(PageNumberPagination):
    page_size = 4


class ReviewPaginator(PageNumberPagination):
    page_size = 10
