from django import forms

from django.contrib.auth.models import User

from .models import Profile, Address, Item, Swap
from allauth.account.forms import SignupForm


class UserRegistrationForm(SignupForm, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
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
            # "location",
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
                    "id": "citysearch",
                }
            ),
            # "location": PlainLocationField(based_fields=["city"]),
        }


class SwapForm(forms.ModelForm):
    class Meta:
        model = Swap
        fields = [
            "message_sent",
        ]
        widgets = {
            "message_sent": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Item message here...",
                    "rows": "5",
                }
            ),
        }


class ContactForm(forms.Form):

    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter message subject here...",
                "rows": "5",
            }
        ),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Item message here...",
                "rows": "5",
            }
        ),
    )
