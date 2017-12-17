from django import forms

from tinymce.widgets import TinyMCE

from .models import Overview


class OverviewForm(forms.ModelForm):
    overview = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Overview
        fields = ('overview',)


def get_overview_form(data=None):
    overview_form = OverviewForm(initial={'overview': data})
    return overview_form
