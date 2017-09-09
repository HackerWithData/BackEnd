from django import forms


class ReviewForm(forms.Form):
    comments = forms.CharField(widget=forms.Textarea, help_text='Please say anything you want.')

    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    project_date = forms.DateField(help_text="Please input the date with YYYY-MM-DD format")
    project_type = forms.CharField(max_length=255)
    project_zipcode = forms.CharField(max_length=20)
    project_cost = forms.IntegerField()
    project_duration = forms.IntegerField()

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    project_address = forms.CharField(max_length=100)

    is_anonymous = forms.BooleanField(required=False)

        #'project_date':forms.DateInput(format="%Y-%m-%d")

# class ReviewForm(forms.ModelForm):
#     model = Review
#
#     def form_valid(self, form):
#         form.instance.contracotr_id = self.kwards.get('contractor_id')
#         return super(ReviewForm, self).form_valid(form)