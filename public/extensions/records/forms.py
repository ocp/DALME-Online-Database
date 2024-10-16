"""Form for records extension."""

from django_currentuser.middleware import get_current_user

from django import forms
from django.db.models import Q

from ida.models import SavedSearch


class RecordFilterForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()

        date_range = self.data.get('date_range')
        if date_range:
            try:
                after, before = date_range.split(',')
            except ValueError:
                self.add_error(
                    'date_range',
                    'Incorrect date format, should be: YYYY,YYYY',
                )

            cleaned_data['date_range'] = [after, before]

        return cleaned_data


class SavedSearchChooserForm(forms.Form):
    id = forms.ChoiceField(required=True, choices=[], label='Saved search')
    name = forms.CharField(required=True, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        user = get_current_user()
        search_list = [
            (i.id, f"{i.name}{' (shared)' if i.owner != user else ''}")
            for i in SavedSearch.objects.filter(Q(owner=user) | Q(shareable=True)).order_by('-creation_timestamp')
        ]
        self.has_saved_searches = len(search_list) > 0
        super().__init__(*args, **kwargs)
        self.fields['id'].choices = [('', '--------'), *search_list]

    def get_context(self):
        context = super().get_context()
        context['has_saved_searches'] = self.has_saved_searches
        return context
