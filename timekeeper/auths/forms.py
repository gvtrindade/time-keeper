from django import forms
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

from auths.models import CustomUser


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control password-input", }), required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control password-input"}), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control password-input"}), required=True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ("old_password", "new_password1", "new_password2")

class PasswordResettingForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={"class": "form-control"}), required=True)

    class Meta:
        model = CustomUser
        fields = ("email")

class PasswordResettingConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control"}), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control"}), required=True)

    def __init__(self, user, *args, **kwargs):
        super(PasswordResettingConfirmForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = CustomUser
        fields = ("new_password1", "new_password2")
