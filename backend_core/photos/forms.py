from models import Photo, BackgroundPhoto
from django import forms

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('img', 'content_type', 'object_id')

        widgets = {
            'object_id': forms.HiddenInput(),
            'content_type': forms.HiddenInput()
        }

class BackgroundPhotoForm(forms.ModelForm):
    class Meta:
        model = BackgroundPhoto
        fields = ('img', 'content_type', 'object_id')

        widgets = {
            'object_id': forms.HiddenInput(),
            'content_type': forms.HiddenInput()
        }


class FileFieldForm(forms.Form):

    img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    fields = ('img', )
    #
    # widgets = {
    #     'object_id': forms.HiddenInput(),
    #     'content_type': forms.HiddenInput(),
    # }