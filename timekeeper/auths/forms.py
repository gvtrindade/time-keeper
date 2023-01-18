from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from auths.models import CustomUser


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control"}), required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control"}), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control"}), required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ("old_password", "new_password1", "new_password2")
