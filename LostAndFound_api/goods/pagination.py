from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    """物品列表分页器"""
    page_query_param = "page"
    page_size_query_param = "size"
    page_size = 2
    max_page_size = 10
