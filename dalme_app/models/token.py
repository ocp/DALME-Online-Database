from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Token(dalmeUuid):
    """Stores information about tokens."""

    object_phrase_id = models.ForeignKey('EntityPhrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    wordform_id = models.ForeignKey('Wordform', to_field='id', db_index=True, on_delete=models.PROTECT)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)
    tags = GenericRelation('Tag')

    def __str__(self):  # noqa: D105
        return self.raw_token
