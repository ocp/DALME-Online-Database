"""Tag model."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin, UuidMixin
from ida.models.tenant import TenantMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Tag(TenantMixin, UuidMixin, TrackingMixin):
    """Store tag information."""

    WORKFLOW = 'WF'  # type of tags used to keep track of general workflow
    CONTROL = 'C'  # general purpose control tags
    TICKET = 'T'  # tags for issue ticket management
    TAG_TYPES = (
        (WORKFLOW, 'Workflow'),
        (CONTROL, 'Control'),
        (TICKET, 'Ticket'),
    )
    TICKET_TAGS = (
        ('bug', 'bug'),
        ('feature', 'feature'),
        ('documentation', 'documentation'),
        ('question', 'question'),
        ('content', 'content'),
    )

    tag_type = models.CharField(max_length=2, choices=TAG_TYPES)
    tag = models.CharField(max_length=55, blank=True)
    tag_group = models.CharField(max_length=255, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=55, blank=True, db_index=True)

    class Meta:
        unique_together = ('tag', 'object_id')

    def __str__(self):
        return self.tag
