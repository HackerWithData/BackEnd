from models import Photo, BackgroundPhoto
from django import forms


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('img',)
        widgets = {'img': forms.ClearableFileInput(attrs={'multiple': True})}


class BackgroundPhotoForm(forms.ModelForm):
    class Meta:
        model = BackgroundPhoto
        fields = ('img', )


class FileFieldForm(forms.Form):
    img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    fields = ('img', )
