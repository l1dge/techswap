from django import forms

from django.contrib.auth.models import User

# from django.forms import fields
from location_field.models.plain import PlainLocationField
from .models import *
from allauth.account.forms import SignupForm

# @todo Look into using allauth as suggested by Bob.
class UserRegistrationForm(SignupForm, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            # "password",
            "first_name",
            "last_name",
        ]

    widgets = {
        "username": forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Username here...",
            }
        ),
        "email": forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Email here...",
            }
        ),
        # "password": forms.PasswordInput(
        #     attrs={
        #         "class": "form-control",
        #     }
        # ),
        "first_name": forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter First Name here...",
            }
        ),
        "last_name": forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Last Name here...",
            }
        ),
    }

    def signup(self, request, user):

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user

    # # @todo Check for lower and uppercase usernames
    # def clean_username(self):
    #     uname = self.cleaned_data.get("username")
    #     if User.objects.filter(username=uname).exists():
    #         raise forms.ValidationError("This username already exists.")

    #     return uname


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "image",
            "phone",
            "bio",
            "birth_date",
        ]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Phone Number here...",
                }
            ),
            "bio": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Bio here...",
                    "rows": 5,
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Birthday here...",
                }
            ),
        }


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "house_num",
            "street",
            "town",
            "city",
            "county",
            "country",
            "zipcode",
        ]
        widgets = {
            "house_num": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "House Number...",
                }
            ),
            "street": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Street...",
                }
            ),
            "town": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Town...",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City...",
                }
            ),
            "county": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "County...",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Country...",
                }
            ),
            "zipcode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Zipcode...",
                }
            ),
        }


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
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
        if User.objects.filter(user__email=e).exists():
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
