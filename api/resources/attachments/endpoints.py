"""API endpoint for managing attachments."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.response import Response

from api.access_policies import BaseAccessPolicy
from ida.models import Attachment

from .serializers import AttachmentSerializer


class AttachmentAccessPolicy(BaseAccessPolicy):
    """Access policies for Attachments endpoint."""

    id = 'attachments-policy'


class Attachments(viewsets.ModelViewSet):
    """API endpoint for managing attachments."""

    permission_classes = [AttachmentAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & AttachmentAccessPolicy]

    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def create(self, request, fmt=None):  # noqa: ARG002
        """Create new attachment record."""
        try:
            new_obj = Attachment()
            new_obj.file = request.data['upload']
            new_obj.save()
            result = {
                'upload': {'id': new_obj.id},
                'files': {
                    'Attachment': {str(new_obj.id): {'filename': str(new_obj.filename), 'web_path': str(new_obj.file)}},
                },
            }
            status = 201
        except Exception as e:  # noqa: BLE001
            result = {'error': 'There was an error processing the file: ' + str(e)}
            status = 400

        return Response(result, status)
