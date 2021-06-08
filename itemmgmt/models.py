from django.db import models
from django.db.models.fields import TextField
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, default=None)
    category = models.ManyToManyField("Category")
    condition = models.CharField(max_length=200)
    image = models.FileField(upload_to="uploads/items")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    swap_comp = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    swap_agrd = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("itemmgmt:itemdet", kwargs={"my_id": self.id})


class ItemImage(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    image = models.FileField(upload_to="uploads/items/images/")

    def __str__(self):
        return f"{self.item.name}"


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Location(models.Model):
    name = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} {self.town} {self.country}"
