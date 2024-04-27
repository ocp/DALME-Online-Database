"""Models for team extension."""

from wagtail.fields import RichTextField

from django.conf import settings
from django.db import models


class TeamRole(models.Model):
    role = models.CharField(max_length=255, help_text='Name of the role.')
    description = models.TextField(help_text='Description of the role.')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='Parent role, if any.',
    )

    def __str__(self):
        return f'{self.role} ({self.parent.role})' if self.parent else f'{self.role}'


class TeamMember(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='team_member_record',
        blank=True,
        null=True,
        help_text='Associated user record, if any.',
    )
    name = models.CharField(max_length=255, help_text='Name as it should appear on the front end.')
    roles = models.ManyToManyField(TeamRole, blank=True, help_text='Project role(s).')
    title = models.CharField(max_length=255, blank=True, help_text='Professional title(s).')
    affiliation = models.CharField(max_length=255, blank=True, help_text='Institutional affiliation.')
    biography = RichTextField(
        features=[
            'bold',
            'italic',
            'link',
            'document-link',
            'code',
            'superscript',
            'subscript',
            'strikethrough',
            'blockquote',
            'reference',
        ],
        blank=True,
        help_text='Short biographical sketch.',
    )
    url = models.URLField(
        blank=True,
        verbose_name='Website',
        help_text='Link to a website or online profile.',
    )
    photo = models.ForeignKey(
        'publicimages.BaseImage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Profile image or avatar.',
    )

    def __str__(self):
        return str(self.name)
