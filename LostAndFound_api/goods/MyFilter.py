# coding:utf-8
# coding:utf-8
from rest_framework import status
from rest_framework.filters import BaseFilterBackend

# 自定义限制过滤器，限制显示条数
from rest_framework.response import Response


class LimitFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            search_name = request.query_params.get('the_type')
            search_name = int(search_name)
        except:
            search_name = -1

        if search_name == -1:
            return queryset
        else:
            the_queryset = queryset.filter(the_type=search_name)
        return the_queryset
