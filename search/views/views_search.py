from rest_framework import viewsets, response
from rest_framework.decorators import action

from admin_api.serializers.serializers_search import SearchListSerializer
from legacies.models import Member


class TestSearchViewSet(
    viewsets.GenericViewSet
):
    queryset = Member.objects.all()
    serializer_class = SearchListSerializer

    @action(methods=['POST'], detail=False)
    def test(self, request, *args, **kwargs):
        serializer = SearchListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)
