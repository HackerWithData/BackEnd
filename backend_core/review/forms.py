from django import forms
from django.utils.translation import ugettext_lazy as _

class ReviewForm(forms.Form):
    comments = forms.CharField(label=_('Comments'), widget=forms.Textarea)

    first_name = forms.CharField(label=_('First Name'), max_length=25)
    last_name = forms.CharField(label=_('Last Name'), max_length=25)
    project_date = forms.DateField(label=_('Project Date'), help_text="YYYY-MM-DD")
    project_type = forms.CharField(label=_('Project Type'), max_length=255)
    project_zipcode = forms.CharField(label=_('Project Zipcode'), max_length=20)
    project_cost = forms.IntegerField(label=_('Project Cost'))
    project_duration = forms.IntegerField(label=_('Project Duration'))

    email = forms.EmailField(label=_('Email'), max_length=254)
    project_address = forms.CharField(label=_('Project Address'), max_length=100)

    is_anonymous = forms.BooleanField(label=_('Is Anonymous?'), required=False)

    #'project_date':forms.DateInput(format="%Y-%m-%d")

# class ReviewForm(forms.ModelForm):
#     model = Review
#
#     def form_valid(self, form):
#         form.instance.contracotr_id = self.kwards.get('contractor_id')
#         return super(ReviewForm, self).form_valid(form)