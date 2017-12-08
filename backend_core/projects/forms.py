from django import forms
from django.utils.translation import ugettext_lazy as __

from .models import ProjectAttachment, ProjectPhoto, Project
from .utils import PROJECT_TYPE, WAITING, get_a_uuid
from users.utils import ROLE_CHOICES, PROFESSIONAL, CONSUMER
from django.core.exceptions import ValidationError
from users.models import User

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
    created_by = forms.ChoiceField(widget=forms.RadioSelect, choices=ROLE_CHOICES, label=__("Who you are?"))
    project_name = forms.CharField(label=__('Project Name'), max_length=100)
    first_name = forms.CharField(label=__('Your First Name'), max_length=64)
    last_name = forms.CharField(label=__('Your Last Name'), max_length=64)
    project_type = forms.ChoiceField(choices=PROJECT_TYPE, label=__('Project Type'), required=False)
    street_address = forms.CharField(label=__('Street Address'))
    street_address2 = forms.CharField(required=False,
                                      widget=forms.TextInput(attrs={'placeholder': __("Apt #,Suite #,...")}))
    county = forms.CharField(label=__('County/City'), max_length=64)
    state = forms.CharField(label=__('State'), max_length=64)
    zipcode = forms.CharField(label=__('Zip Code'), max_length=10)
    # country = forms.CharField(label=__('Country'), max_length=10)
    # TODO: need to add a calender widget
    start_date = forms.DateField(label=__('Start Date'), widget=forms.SelectDateWidget())
    end_date = forms.DateField(label=__('End Date'), widget=forms.SelectDateWidget())
    project_description = forms.CharField(label=__('Project Description'), required=False, widget=forms.Textarea(
        attrs={'placeholder': __('(Optional) Please briefly describe your project')}))
    attachment_type = forms.CharField(label=__('Attachment Type'), required=False, max_length=64)
    project_attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    project_photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
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
    professional_hoome_id = forms.CharField(label=__("Professional Hoome ID"), required=False)
    homeowner_hoome_id = forms.CharField(label=__("Homeowner Hoome ID"), required=False)

    def clean(self):
        cleaned_data = super(ProjectFormDirectCreate, self).clean()
        created_by = cleaned_data.get('created_by')
        if created_by == PROFESSIONAL:
            homeowner_hoome_id = cleaned_data.get('homeowner_hoome_id', None)
            if not homeowner_hoome_id:
                raise ValidationError(message='hoome id cannot be empty', code='homeowner_hoome_id_error')
            else:
                try:
                    user = User.objects.get(hoome_id=homeowner_hoome_id)
                except:
                    raise ValidationError(message='The hoome id does not exist', code='homeowner_hoome_id_error')
                if user.role == PROFESSIONAL:
                    raise ValidationError(message='It is a professional user', code='homeowner_hoome_id_error')
        elif created_by == CONSUMER:
            professional_hoome_id = cleaned_data.get('professional_hoome_id', None)
            if not professional_hoome_id:
                raise ValidationError(message='hoome id cannot be empty', code='professional_hoome_id_error')
            else:
                try:
                    user = User.objects.get(hoome_id=professional_hoome_id)
                except:
                    raise ValidationError(message='The hoome id does not exist', code='professional_hoome_id_error')
                if user.role == CONSUMER:
                    raise ValidationError(message='It is a consumer user', code='professional_hoome_id_error')
        return cleaned_data

    def error_info(self):
        e = self.errors.as_data()
        errors = e.get('__all__', None)
        form_errors = {}
        if errors is not None:
            for error in errors:
                form_errors.update({error.code: error.message})
        return form_errors

# class ProjectFormAfterLogin(ProjectForm):
#     professional_hoome_id = forms.CharField(label=__("Professional Hoome ID"))


class MilestoneForm(forms.Form):
    amount = forms.IntegerField(min_value=50, required=True)
