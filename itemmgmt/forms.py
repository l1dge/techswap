from django import forms
from django.forms import fields

from .models import Item


class ItemForm(forms.ModelForm):
    more_images = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "multiple": True}),
    )

    class Meta:
        model = Item
        fields = [
            "title",
            "category",
            "description",
            "image",
            "condition",
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
            "condition": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Item condition here...",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Item location here...",
                }
            ),
        }
