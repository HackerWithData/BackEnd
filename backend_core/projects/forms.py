from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import formset_factory
from django.forms.models import model_to_dict

from .models import (
    ProjectAttachment,
    ProjectPhoto,
    Project,
    PROJECT_TYPE,
    WAITING,
)
from .utils import get_a_uuid
from django.core.exceptions import ValidationError
from users.models import User, ROLE_CHOICES, PROFESSIONAL, CONSUMER


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
    created_by = forms.ChoiceField(label=_("Choose your identity*"), widget=forms.RadioSelect, choices=ROLE_CHOICES)
    project_name = forms.CharField(label=_('Project Name*'), max_length=100,
                                   widget=forms.TextInput(attrs={'placeholder': _('Choose a name for your project')}))
    project_type = forms.ChoiceField(choices=PROJECT_TYPE, label=_('Project Type*'))
    contract_price = forms.IntegerField(label=_('Contract Price*'), min_value=0)
    start_date = forms.DateField(label=_('Start Date*'), widget=forms.SelectDateWidget())
    end_date = forms.DateField(label=_('End Date*'), widget=forms.SelectDateWidget())
    first_name = forms.CharField(label=_("Homeowner's First Name"), max_length=64, required=False)
    last_name = forms.CharField(label=_("Honemowner's Last Name"), max_length=64, required=False)
    project_description = forms.CharField(label=_('Project Description'), required=False,
                                          widget=forms.Textarea(
                                              attrs={'placeholder': _(
                                                  '(Optional) Tell us more about your project.')}))
    street_address = forms.CharField(label=_('Street Address'), required=False)
    street_address2 = forms.CharField(label=_('Apt #, Suite #, ...'), required=False,
                                      widget=forms.TextInput(attrs={'placeholder': _("(Optional) Apt #,Suite #,...")}))
    county = forms.CharField(label=_('County/City'), max_length=64, required=False)
    state = forms.CharField(label=_('State'), max_length=64, required=False)
    zipcode = forms.CharField(label=_('Zip Code'), max_length=10, required=False)
    # country = forms.CharField(label=__('Country'), max_length=10)
    # TODO: need to add a calender widget

    # project_cost = forms.IntegerField(label=__('Total Project Cost shown in Contract*'),min_value=0, required=True)
    attachment_type = forms.CharField(label=_('Attachment Type'), required=False, max_length=64)
    project_attachment = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False,
        help_text=_('upload any documents or contracts that might be helpful in explaining your project brief here.'))
    project_photo = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False,
        help_text=_('upload any photos that might be helpful in explaining your project brief here.'))

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
                          # project_cost=self.cleaned_data['project_cost'],
                          contract_price=self.cleaned_data['contract_price'],
                          start_date=self.cleaned_data['start_date'],
                          end_date=self.cleaned_data['end_date'],
                          project_description=self.cleaned_data['project_description'],
                          created_by=self.cleaned_data['created_by'],
                          project_status=WAITING)
        project.uuid = get_a_uuid(Project)
        if commit:
            project.save()
        return project


class ProjectEditForm(forms.Form):
    # project_name = forms.CharField(label=__('Project Name'), max_length=100, disabled=True)
    # project_type = forms.ChoiceField(choices=PROJECT_TYPE, label=__('Project Type'), disabled=True)
    # contract_price = forms.IntegerField(label=__('Contract Price'), min_value=0, disabled=True)
    # start_date = forms.DateField(label=__('Start Date'), widget=forms.SelectDateWidget(), disabled=True)
    # end_date = forms.DateField(label=__('End Date'), widget=forms.SelectDateWidget(), disabled=True)
    first_name = forms.CharField(label=_("Homeowner's First Name"), max_length=64, required=False)
    last_name = forms.CharField(label=_("Honemowner's Last Name"), max_length=64, required=False)
    project_description = forms.CharField(label=_('Project Description'), required=False,
                                          widget=forms.Textarea(
                                              attrs={'placeholder': _(
                                                  '(Optional) Tell us more about your project.')}))
    street_address = forms.CharField(label=_('Street Address'), required=False)
    street_address2 = forms.CharField(label=_('Apt #, Suite #, ...'), required=False,
                                      widget=forms.TextInput(attrs={'placeholder': _("(Optional) Apt #,Suite #,...")}))
    county = forms.CharField(label=_('County/City'), max_length=64, required=False)
    state = forms.CharField(label=_('State'), max_length=64, required=False)
    zipcode = forms.CharField(label=_('Zip Code'), max_length=10, required=False)

    def update(self, instance, commit=True):
        if instance:
            instance.first_name = self.cleaned_data['first_name']
            instance.last_name = self.cleaned_data['last_name']
            instance.street_address = self.cleaned_data['street_address']
            instance.street_address2 = self.cleaned_data['street_address2']
            instance.county = self.cleaned_data['county']
            instance.state = self.cleaned_data['state']
            instance.zipcode = self.cleaned_data['zipcode']
            instance.project_description = self.cleaned_data['project_description']

        if commit:
            instance.save()
        return instance


class ProjectFormDirectCreate(ProjectForm):
    professional_hoome_id = forms.CharField(label=_("Enter the Contractor/Meister's Hoome ID*"), required=False)
    homeowner_hoome_id = forms.CharField(label=_("Enter the Homeowner's Hoome ID*"), required=False)

    def clean(self):
        cleaned_data = super(ProjectFormDirectCreate, self).clean()
        created_by = cleaned_data.get('created_by')
        if created_by == PROFESSIONAL:
            homeowner_hoome_id = cleaned_data.get('homeowner_hoome_id', None)
            if not homeowner_hoome_id:
                raise ValidationError(message=_('Hoome id cannot be empty.'), code='homeowner_hoome_id_error')
            else:
                try:
                    user = User.objects.get(hoome_id=homeowner_hoome_id)
                except User.DoesNotExist:
                    raise ValidationError(message=_("Homeowener's Hoome id does not exist"),
                                          code='homeowner_hoome_id_error')
                if user.role == PROFESSIONAL:
                    raise ValidationError(message=_("Homeowener's Hoome id does not exist"),
                                          code='homeowner_hoome_id_error')
        elif created_by == CONSUMER:
            professional_hoome_id = cleaned_data.get('professional_hoome_id', None)
            if not professional_hoome_id:
                raise ValidationError(message=_('Hoome id cannot be empty'), code='professional_hoome_id_error')
            else:
                try:
                    user = User.objects.get(hoome_id=professional_hoome_id)
                except User.DoesNotExist:
                    raise ValidationError(message=_("Contractor/Meister's Hoome id does not exist"),
                                          code='professional_hoome_id_error')
                if user.role == CONSUMER:
                    raise ValidationError(message=_("Contractor/Meister's Hoome id does not exist"),
                                          code='professional_hoome_id_error')
        return cleaned_data

        # def error_info(self):
        #     e = self.errors.as_data()
        #     errors = e.get('__all__', None)
        #     form_errors = {}
        #     if errors is not None:
        #         for error in errors:
        #             form_errors.update({error.code: error.message})
        #     return form_errors


# class ProjectFormAfterLogin(ProjectForm):
#     professional_hoome_id = forms.CharField(label=__("Professional Hoome ID"))


class MilestoneForm(forms.Form):
    amount = forms.IntegerField(min_value=500, required=True)


def get_project_form(request, professional_type=None, lic_id=None):
    if request.method == "GET":
        if professional_type and lic_id:
            if request.user.is_authenticated:
                project_form = ProjectForm(
                    initial={
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                    }
                )
            else:
                project_form = ProjectForm()
        else:
            project_form = ProjectFormDirectCreate()
        return project_form
    elif request.method == "POST":
        if professional_type and lic_id:
            project_form = ProjectForm(request.POST, request.FILES)
        else:
            project_form = ProjectFormDirectCreate(request.POST, request.FILES)
        return project_form


def get_milestone_formset(request):
    milestoneformset = formset_factory(MilestoneForm)
    if request.method == "GET":
        milestone_formset = milestoneformset()
        return milestone_formset
    elif request.method == "POST":
        milestone_formset = milestoneformset(request.POST)
        return milestone_formset


def get_project_edit_form(request, project):
    if request.method == "GET":
        project_edit_form = ProjectEditForm(initial=model_to_dict(project))
        return project_edit_form
    elif request.method == "POST":
        project_edit_form = ProjectEditForm(request.POST)
        return project_edit_form


def get_milestone_form(request):
    if request.method == "POST":
        milestone_form = MilestoneForm(request.POST)
        return milestone_form
    elif request.method == "GET":
        milestone_form = MilestoneForm(initial={'amount': 2000})
        return milestone_form


def get_project_attachment_form(request):
    if request.method == "POST":
        return ProjectAttachmentForm(request.POST, request.FILES)
    else:
        return ProjectAttachmentForm()
