from django import forms
import string
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Username"}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={"class": "form-control text-dark mt-3", "placeholder": "Password"}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label = ""

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control text-dark", "placeholder": "Username"}))
    email = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control text-dark mt-3", "placeholder": "Email address"}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={"class": "form-control text-dark mt-3", "placeholder": "Password"}))
    confirm_password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={"class": "form-control text-dark mt-3", "placeholder": "Confirm password"}))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label = ""

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("confirm_password")

        if "@" not in email:
            raise forms.ValidationError(_("Please insert an email address!"), code="invalid")
        
        if " " in username:
            raise forms.ValidationError(_("Please don't use spaces in your username!"), code="invalid")

        if password != password_confirm:
            raise forms.ValidationError(_("The passwords do not match!"), code="invalid")
        elif len(password) < 4:
            raise forms.ValidationError(_("Please choose a longer password! (4 characters minimum)"), code="invalid")

        has_upper = False
        has_sign = False
        for letter in password:
            if letter.isupper():
                has_upper = True
            if letter in string.punctuation:
                has_sign = True
        
        if has_upper == False:
            raise forms.ValidationError(_("Your password needs at least ONE uppercase letter!"), code="invalid")
        if has_sign == False:
            raise forms.ValidationError(_(f"Your password needs at least ONE punctuation character! ({string.punctuation})"), code="invalid")

        return cleaned_data