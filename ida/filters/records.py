"""Interface for the ida.filters.records module."""

import django_filters as filters

from ida.forms import RecordFilterForm
from ida.models import AttributeType, Collection, Record

BOOLEAN_CHOICES = [('true', 'Yes'), ('false', 'No')]


def corpus_choices():
    return AttributeType.objects.get(name='corpus').options.get_values(serialize=False)


def collection_choices():
    return AttributeType.objects.get(name='collection').options.get_values(serialize=False)


def record_type_choices():
    return AttributeType.objects.get(name='record_type').options.get_values(serialize=False)


def locale_choices():
    return AttributeType.objects.get(name='locale').options.get_values(serialize=False)


class RecordOrderingFilter(filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('name', 'Name'),
            ('-name', 'Name (descending)'),
            ('record_type', 'Type'),
            ('-record_type', 'Type (descending)'),
            ('date', 'Date'),
            ('-date', 'Date (descending)'),
            ('short_name', 'Short name'),
            ('-short_name', 'Short name (descending)'),
        ]

    @staticmethod
    def get_value(field, value):
        if not value:
            return None
        return next((v for v in value if v and v.endswith(field)), None)

    def filter(self, qs, value):
        if value:
            for field in value:
                field = f'{field}__year' if field.endswith('date') else field  # noqa: PLW2901
                field = f'{field}__name' if field.endswith('record_type') else field  # noqa: PLW2901
                return qs.order_by(field)
        return qs.order_by('name')


class RecordFilter(filters.FilterSet):
    wf_status = filters.NumberFilter(field_name='workflow__wf_status', lookup_expr='iexact')
    wf_stage = filters.NumberFilter(field_name='workflow__stage', lookup_expr='iexact')
    help_flag = filters.BooleanFilter(field_name='workflow__help_flag')
    is_public = filters.BooleanFilter(field_name='workflow__is_public')
    ingestion_done = filters.BooleanFilter(field_name='workflow__ingestion_done')
    transcription_done = filters.BooleanFilter(field_name='workflow__transcription_done')
    markup_done = filters.BooleanFilter(field_name='workflow__markup_done')
    review_done = filters.BooleanFilter(field_name='workflow__review_done')
    parsing_done = filters.BooleanFilter(field_name='workflow__parsing_done')

    name = filters.CharFilter(label='Name', lookup_expr='icontains')
    record_type = filters.MultipleChoiceFilter(label='Type', choices=record_type_choices, method='filter_type')
    date_range = filters.DateFromToRangeFilter(label='Date Range', method='filter_date_range')

    corpus = filters.ChoiceFilter(label='Corpus', choices=corpus_choices, method='filter_corpus')
    collection = filters.ChoiceFilter(label='Collection', choices=collection_choices, method='filter_collection')
    has_image = filters.ChoiceFilter(label='Has Image', method='filter_image', choices=BOOLEAN_CHOICES)
    has_transcription = filters.ChoiceFilter(
        label='Has Transcription', method='filter_transcription', choices=BOOLEAN_CHOICES
    )
    locale = filters.ChoiceFilter(label='Locale', choices=locale_choices, method='filter_locale')

    order_by = RecordOrderingFilter()

    class Meta:
        model = Record
        form = RecordFilterForm
        fields = [
            'name',
            'record_type',
            'date_range',
            'corpus',
            'collection',
            'has_transcription',
            'has_image',
            'locale',
            'order_by',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for definition in self.filters.values():
            definition.field.label_suffix = ''

    def filter_type(self, queryset, name, value):  # noqa: ARG002
        return queryset.filter(record_type__id__in=value)

    def filter_date_range(self, queryset, name, value):  # noqa: ARG002
        queryset = queryset.filter(attributes__attribute_type__name__in=['date', 'start_date', 'end_date']).distinct()

        after, before = value
        if after:
            queryset = queryset.filter(attributes__value__year__gte=int(after))
        if before:
            queryset = queryset.filter(attributes__value__year__lte=int(before))

        return queryset

    def filter_corpus(self, queryset, name, value):  # noqa: ARG002
        try:
            corpus = Collection.objects.get(pk=value, is_corpus=True)
        except Collection.DoesNotExist:
            return queryset.none()
        return queryset.filter(collections__collection_id__in=[c.object_id for c in corpus.members.all()])

    def filter_collection(self, queryset, name, value):  # noqa: ARG002
        return queryset.filter(collections__collection_id=value)

    def filter_image(self, queryset, name, value):  # noqa: ARG002
        value = value == 'true'
        return queryset.exclude(folios__page__dam_id__isnull=value)

    def filter_transcription(self, queryset, name, value):  # noqa: ARG002
        value = value == 'true'
        return queryset.exclude(folios__transcription__isnull=value)

    def filter_locale(self, queryset, name, value):  # noqa: ARG002
        return queryset.filter(locale__id=value)
