"""Customize staticfiles storage logic."""

import structlog
from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage

from django.db import connection

from ida.context import get_current_tenant

logger = structlog.get_logger(__name__)


class StaticStorage(S3ManifestStaticStorage):
    """Multitenant aware staticfiles storage class for S3."""

    key = 'static'

    @property
    def schema(self):
        """Get the tenant schema name."""
        try:
            return get_current_tenant().schema_name
        except RuntimeError:
            return connection.tenant.schema_name

    @property
    def location(self):
        """Get the schema qualified filepath."""
        return f'{self.key}/{self.schema}'


class MediaStorage(S3Boto3Storage):
    """Multitenant aware media files storage class for S3."""

    key = 'media'

    @property
    def schema(self):
        """Get the tenant schema name."""
        try:
            return get_current_tenant().schema_name
        except RuntimeError:
            return connection.tenant.schema_name

    @property
    def location(self):
        """Get the schema qualified filepath."""
        return f'{self.key}/{self.schema}'
