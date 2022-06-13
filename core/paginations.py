from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination,
)


class DefaultCursorPagination(CursorPagination):
    page_size = 20
    cursor_query_param = "id"
    ordering = "-id"


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    ordering = "-id"
