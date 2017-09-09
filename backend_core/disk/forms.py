from django import forms

class UserForm(forms.Form):
    userName = forms.CharField(max_length=20)
    uploadFile = forms.FileField()


class ImageForm(forms.ModelForm):
    userName = forms.CharField(max_length=20)
    image = forms.ImageField()

