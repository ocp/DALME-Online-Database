"""Permissions model."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Permission(UuidMixin, TrackingMixin):
    """Stores object-level permissions information."""

    principal = GenericForeignKey('principal_type', 'principal_id')
    principal_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        related_name='cperm_principals',
    )
    principal_id = models.PositiveIntegerField(db_index=True, null=True)
    content = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        related_name='cperm_objects',
    )
    object_id = models.CharField(max_length=36, db_index=True)
    is_default = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_remove = models.BooleanField(default=False)

    class Meta:
        unique_together = ('content_type', 'object_id', 'principal_type', 'principal_id')
