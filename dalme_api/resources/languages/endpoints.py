"""API endpoint for managing languages."""
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from ida.models import LanguageReference

from .serializers import LanguageReferenceSerializer


class Languages(DALMEBaseViewSet):
    """API endpoint for managing languages."""

    permission_classes = [GeneralAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope]

    queryset = LanguageReference.objects.all()
    serializer_class = LanguageReferenceSerializer
    filterset_fields = ['id', 'name', 'is_dialect', 'parent__name', 'iso6393', 'glottocode']
    search_fields = ['id', 'name', 'is_dialect', 'parent__name', 'iso6393', 'glottocode']
    ordering_fields = ['id', 'name', 'is_dialect', 'parent', 'iso6393', 'glottocode']
    ordering = ['name']
