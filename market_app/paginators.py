from rest_framework.pagination import PageNumberPagination


class AdvirtesementPaginator(PageNumberPagination):
    page_size = 4
