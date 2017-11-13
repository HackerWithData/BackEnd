from django import forms
from models import Overview
from tinymce.widgets import TinyMCE


class OverviewForm(forms.ModelForm):
    overview = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Overview
        fields = ('overview',)
