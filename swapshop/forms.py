from django import forms
from django.contrib.auth.models import User
from django.forms import fields
from location_field.models.plain import PlainLocationField
from .models import *

# @todo Look into using allauth as suggested by Bob.
class AppUserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = AppUser
        fields = ["username", "password", "email", "full_name", "address"]

    # @todo Check for lower and upercase usernames
    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("This username already exists.")

        return uname


class AppUserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class PasswordForgotForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the email used for your user account...",
            }
        )
    )

    # @todo Change the check below to the negative i.e if not etc.
    def clean_email(self):
        e = self.cleaned_data.get("email")
        if AppUser.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError("User with this account does not exist..")
        return e


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
                "placeholder": "Enter New Password",
            }
        ),
        label="New Password",
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
                "placeholder": "Confirm New Password",
            }
        ),
        label="Confirm New Password",
    )

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError("New Passwords did not match!")
        return confirm_new_password


class ItemForm(forms.ModelForm):
    more_images = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "multiple": True}),
    )

    class Meta:
        model = Item
        exclude = ["created_by"]
        fields = [
            "title",
            "category",
            "description",
            "image",
            "condition",
            "city",
            "location",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Item title here...",
                }
            ),
            "category": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Item description here...",
                    "rows": "5",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "condition": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Item condition here...",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter City location here...",
                }
            ),
            "location": PlainLocationField(based_fields=["city"]),
        }
