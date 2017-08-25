from django import forms


class SearchForm(forms.Form):
    target_type = forms.CharField(max_length=100)
    keywords = forms.CharField(max_length=200)
    zipcode = forms.CharField(min_length=5, max_length=5)

    # TODO: update type validation function
    def clean_type(self):
        target_type = self.cleaned_data['type']
        return target_type

    # TODO: update keywords validation function
    def clean_keywords(self):
        keywords = self.cleaned_data['keywords']
        return keywords

    # TODO: update zipcode validation function
    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        return zipcode
