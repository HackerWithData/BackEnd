from django import forms
from django.utils.translation import ugettext_lazy as __

from .models import ProjectAttachment, ProjectPhoto, Project
from .utils import PROJECT_TYPE, WAITING, get_a_uuid
from users.utils import ROLE_CHOICES


class ProjectAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAttachment
        fields = ('attachment_type', 'project_attachment')
        widgets = {'project_attachment': forms.ClearableFileInput(attrs={'multiple': True})}


class ProjectPhotoForm(forms.ModelForm):
    class Meta:
        model = ProjectPhoto
        fields = ('project_photo',)
        widgets = {'project_photo': forms.ClearableFileInput(attrs={'multiple': True})}


class ProjectForm(forms.Form):
    # TODO: need a google address autocompeletion/correction
    created_by = forms.ChoiceField(widget=forms.RadioSelect, choices=ROLE_CHOICES, label=__("Choose your idenity*"))
    project_name = forms.CharField(label=__('Choose a name for your project*'), max_length=100)
    first_name = forms.CharField(label=__("Homeowner's First Name*"), max_length=64)
    last_name = forms.CharField(label=__("Honemowner's Last Name*"), max_length=64)
    project_type = forms.ChoiceField(choices=PROJECT_TYPE, label=__('Project Type*'), required=False)
    project_description = forms.CharField(label=__('Tell us more about your project'), required=False,
                                          widget=forms.Textarea(
                                              attrs={'placeholder': __(
                                                  '(Optional) Please briefly describe your project.')}))
    street_address = forms.CharField(label=__('Street Address*'))
    street_address2 = forms.CharField(label=__('Apt #, Suite #, ...'), required=False,
                                      widget=forms.TextInput(attrs={'placeholder': __("(Optional) Apt #,Suite #,...")}))
    county = forms.CharField(label=__('County/City*'), max_length=64)
    state = forms.CharField(label=__('State*'), max_length=64)
    zipcode = forms.CharField(label=__('Zip Code*'), max_length=10)
    # country = forms.CharField(label=__('Country'), max_length=10)
    # TODO: need to add a calender widget
    start_date = forms.DateField(label=__('Start Date*'), widget=forms.SelectDateWidget())
    end_date = forms.DateField(label=__('End Date*'), widget=forms.SelectDateWidget())

    attachment_type = forms.CharField(label=__('Attachment Type'), required=False, max_length=64)
    project_attachment = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False,
        help_text=__('upload any documents or contracts that might be helpful in explaining your project brief here.'))
    project_photo = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False,
        help_text=__('upload any photos that might be helpful in explaining your project brief here.'))
    # project_status = forms.CharField(label=__('Project Status'),)
    # professional_type = forms.CharField(label=__('Project Type'))
    # lic_id = forms.CharField(label=__('Lic Id'))

    def save_project(self, commit=True):
        project = Project(project_name=self.cleaned_data['project_name'],
                          first_name=self.cleaned_data['first_name'],
                          last_name=self.cleaned_data['last_name'],
                          project_type=self.cleaned_data['project_type'],
                          street_address=self.cleaned_data['street_address'],
                          street_address2=self.cleaned_data['street_address2'],
                          county=self.cleaned_data['county'],
                          state=self.cleaned_data['state'],
                          zipcode=self.cleaned_data['zipcode'],
                          # country=project_form.cleaned_data['country'],
                          # cost=project_form.cleaned_data['project_cost'],
                          start_date=self.cleaned_data['start_date'],
                          end_date=self.cleaned_data['end_date'],
                          project_description=self.cleaned_data['project_description'],
                          created_by=self.cleaned_data['created_by'],
                          project_status=WAITING)
        project.uuid = get_a_uuid(Project)
        if commit:
            project.save()
        return project


class ProjectFormDirectCreate(ProjectForm):
    professional_hoome_id = forms.CharField(label=__("Enter the Professional's Hoome ID*"), required=False)
    homeowner_hoome_id = forms.CharField(label=__("Enter the Homeowner's Hoome ID*"), required=False)


# class ProjectFormAfterLogin(ProjectForm):
#     professional_hoome_id = forms.CharField(label=__("Professional Hoome ID"))


class MilestoneForm(forms.Form):
    amount = forms.IntegerField(min_value=0, required=True)
#
# class MilestoneBaseFormSet(forms.formset.BaseFormSet):
#     def clean(self):
#         if any(self.errors):
#             return
#
#         for form in self.froms:
#             if form.cleaned_data:
#                 amount = form.cleaned_data['amount']
#                 try:
#                     int(amount)
#                 except:
#                     raise forms.ValidationError(
#                         'Amount must a number',
#                         code='not a number '
#                     )
#                 if amount > 0:
#                     pass
#                 else:
#                     raise forms.ValidationError(
#                         'Amount must a number greater than 0',
#                         code='negative number '
#                     )

