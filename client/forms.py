from django import forms

from .models import Client


class UploadImgForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('img',)
