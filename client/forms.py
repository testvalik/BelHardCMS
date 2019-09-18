from django import forms

from .models import Client, Skills


class UploadImgForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('img',)


class AddSkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ('skills',)
