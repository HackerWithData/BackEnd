from models import ProjectAttachment, ProjectPhoto
from django import forms
from django.utils.translation import ugettext_lazy as __


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
    REMODEL = "R"
    NEWBUILT = "N"
    PROJECT_TYPE = (
        ("", '-----'),
        (REMODEL, __('REMODEL')),
        (NEWBUILT, __("NEW BUILT HOUSE")),
    )
    # TODO: need a google address autocompeletion/correction
    project_name = forms.CharField(label=__('Project Name'), max_length=100)
    first_name = forms.CharField(label=__('First Name'), max_length=64)
    last_name = forms.CharField(label=__('Last Name'), max_length=64)
    project_type = forms.ChoiceField(choices=PROJECT_TYPE, label=__('Project Type'), required=False)
    street_address = forms.CharField(label=__('Street Address'))
    street_address2 = forms.CharField(required=False,
                                      widget=forms.TextInput(attrs={'placeholder': __("Apt #,Suite #,...")}))
    county = forms.CharField(label=__('County/City'), max_length=64)
    state = forms.CharField(label=__('State'), max_length=64)
    zipcode = forms.CharField(label=__('Zip Code'), max_length=10)
    #country = forms.CharField(label=__('Country'), max_length=10)
    #TODO: need to add a calender widget
    start_date = forms.DateField(label=__('Start Date'), widget=forms.SelectDateWidget())
    # end_date = forms.DateField(label=__('End Date'), help_text="YYYY-MM-DD")
    project_description = forms.CharField(label=__('Project Description'), required=False, widget=forms.Textarea(
                                          attrs={'placeholder': __('(Optional) Please briefly describe your project')}))
    attachment_type = forms.CharField(label=__('Attachment Type'), required=False, max_length=64)
    project_attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    project_photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    # project_status = forms.CharField(label=__('Project Status'),)
    # professional_type = forms.CharField(label=__('Project Type'))
    # lic_id = forms.CharField(label=__('Lic Id'))



