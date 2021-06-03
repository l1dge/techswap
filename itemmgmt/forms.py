from django import forms
from django.forms import fields

from .models import Items


class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ["name", "category", "description", "condition", "location", "photoID"]
