from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re


def name_validator(name):
    if not name.isalpha():
        raise ValidationError('name must contain only alphabetic characters', code='name_error')

#doesn;t need to use validator for date. suggest to use SelectDateWidget:
#https://docs.djangoproject.com/en/1.11/ref/forms/widgets/#selectdatewidget
def date_validator(date):
    year = date.year
    month = date.month
    day = date.day
    month_30 = [4, 6, 9, 11]
    month_31 = [1, 3, 5, 7, 8, 10, 12]
    if month in month_30 and (day <= 0 or day > 30):
        raise ValidationError(_('invalid date'), code='date_error')
    elif month in month_31 and (day <= 0 or day > 31):
        raise ValidationError(_('invalid date'), code='date_error')
    elif month == 2:
        if year % 4 == 0 and year % 100 != 0:
            if day <= 0 or day > 29:
                raise ValidationError(_('invalid date'), code='date_error')
        else:
            if day <= 0 or day > 28:
                raise ValidationError(_('invalid date'), code='date_error')

def zipcode_validator(zipcode):
    rex = re.compile(r'^\d{5}(?:[-\s]\d{4})?$')
    if not rex.match(zipcode):
        raise ValidationError(_('zipcode format should be xxxxx or xxxxx-xxxx'), code='zipcode_error')


def positive_int_validator(num):
    if num < 0:
        raise ValidationError(_('cannot be a negative number'), code='cost_error')


def email_validator(email):
    rex = re.compile(r'^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$')
    if not rex.match(email):
        raise ValidationError(_('invalid email address'), code='email_error')


class ReviewForm(forms.Form):
    comments = forms.CharField(label=_('Comments'), widget=forms.Textarea)
    first_name = forms.CharField(label=_('First Name'), max_length=25, validators=[name_validator])
    last_name = forms.CharField(label=_('Last Name'), max_length=25, validators=[name_validator])
    project_date = forms.DateField(label=_('Project Date'), help_text="YYYY-MM-DD", validators=[date_validator])
    project_type = forms.CharField(label=_('Project Type'), max_length=255)
    project_zipcode = forms.CharField(label=_('Project Zipcode'), max_length=20, validators=[zipcode_validator])
    project_cost = forms.IntegerField(label=_('Project Cost'), validators=[positive_int_validator])
    project_duration = forms.IntegerField(label=_('Project Duration'), validators=[positive_int_validator])

    email = forms.CharField(label=_('Email'), max_length=254, validators=[email_validator])
    project_address = forms.CharField(label=_('Project Address'), max_length=100)

    is_anonymous = forms.BooleanField(label=_('Is Anonymous?'), required=False)


    #'project_date':forms.DateInput(format="%Y-%m-%d")

# class ReviewForm(forms.ModelForm):
#     model = Review
#
#     def form_valid(self, form):
#         form.instance.contracotr_id = self.kwards.get('contractor_id')
#         return super(ReviewForm, self).form_valid(form)