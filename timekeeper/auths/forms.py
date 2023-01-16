from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control"}), required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control"}), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control"}), required=True)

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")
