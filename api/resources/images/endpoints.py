"""API endpoint for managing DAM images."""

import json
from json import JSONDecodeError

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import action
from rest_framework.response import Response

from api.access_policies import BaseAccessPolicy
from api.base_viewset import IDABaseViewSet
from ida.models.resourcespace import rs_api_query, rs_resource

from .serializers import RSImageSerializer

RS_API_PARAMS = {
    'q': 'param1',
    'n': 'param5',
    'size': 'param8',
}


class ImageAccessPolicy(BaseAccessPolicy):
    """Access policies for Images endpoint."""

    id = 'images-policy'


class Images(IDABaseViewSet):
    """API endpoint for managing DAM images."""

    permission_classes = [ImageAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & ImageAccessPolicy]

    queryset = rs_resource.objects.filter(resource_type=1, archive=0, ref__gte=0)
    serializer_class = RSImageSerializer
    search_fields = ['ref', 'title', 'country', 'field12', 'field8', 'field3', 'field51', 'field79']
    ordering_fields = ['ref', 'title', 'country', 'field12', 'field8', 'field3', 'field51', 'field79']
    ordering = ['ref']
    search_dict = {'collections': 'collections__name'}
    filterset_fields = [
        'ref',
        'title',
        'resource_type',
        'country',
        'field12',
        'field8',
        'field3',
        'field51',
        'field79',
        'collections',
    ]

    def get_queryset(self, *args, **kwargs):
        """Return filtered queryset."""
        qs = super().get_queryset(*args, **kwargs)
        return qs.values('ref', 'field8') if self.options_view else qs

    @action(detail=False)
    def rs_api(self, request, *args, **kwargs):  # noqa: ARG002
        """Query the RS/DAM API."""
        try:
            query_params = {v: self.request.GET.get(k) for k, v in RS_API_PARAMS.items() if self.request.GET.get(k)}
            # if RS API returns 0s for records exceeding the row count use:
            # row_cutoff = query_params.get('param5', '20')
            response = rs_api_query(**query_params)
            try:
                return Response(json.loads(response.text), 201)  # [:int(row_cutoff)]
            except JSONDecodeError:
                return Response('Your search did not return any results.', 201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)
