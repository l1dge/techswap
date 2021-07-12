from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import TextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from location_field.models.plain import PlainLocationField
from django.utils.text import slugify

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import random

# Item Management
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        value = self.slug
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


ITEM_CONDITION = (
    (s, s)
    for s in ("Like New", "Excellent", "Good", "Used", "Poor", "Spares or Repair")
)


class Item(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default="", editable=False, max_length=255)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=500, default=None)
    image = models.FileField(upload_to="items")
    condition = models.CharField(max_length=50, choices=ITEM_CONDITION)
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=["city"], zoom=7)
    swap_comp = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    swap_agrd = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} {self.slug}"

    def get_absolute_url(self):
        kwargs = {"pk": self.id, "slug": self.slug, "my_id": self.id}
        return reverse("itemdetail", kwargs=kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        value = self.slug
        self.slug = slugify(
            value,
            allow_unicode=True,
        )
        super().save(*args, **kwargs)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.FileField(upload_to="items/multimages/")

    def __str__(self):
        return self.item.title


class WishList(models.Model):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WishList: {self.id}"


class WishListItem(models.Model):
    item_list = models.ForeignKey(WishList, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"WishList: {self.item_list.id} WishlistItem: {self.id}"


class SwapList(models.Model):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SwapList: {self.id}"


class SwapListItem(models.Model):
    item_list = models.ForeignKey(SwapList, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"SwapList: {self.item_list.id} SwaplistItem: {self.id}"


SWAP_STATUS = (
    (s, s)
    for s in (
        "Item Active",
        "Item Wanted",
        "Swap Initiated",
        "Swap Agreed",
        "Swap Complete",
        "Swap Cancelled",
    )
)


class Swap(models.Model):
    swap_list = models.ForeignKey(SwapList, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    email_from = models.EmailField(null=True, blank=True)
    email_to = models.EmailField(null=True, blank=True)
    swap_status = models.CharField(max_length=50, choices=SWAP_STATUS)
    message_sent = models.TextField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    swap_completed = models.BooleanField(default=False, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Swap: {self.id}"


class Location(models.Model):
    name = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} {self.town} {self.country}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True, blank=True)
    image = models.FileField(
        upload_to="profile_images",
        null=True,
        blank=True,
        default="profile_images/dummy-avatar.png",
    )
    rating = models.IntegerField(default=0, blank=True)
    feedback = models.ManyToManyField("Feedback", related_name="Feedback", blank=True)
    items = models.ManyToManyField(Item, related_name="Items", blank=True)
    bio = models.TextField(_("bio"), max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.rating} {self.feedback}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Address(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    house_num = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    town = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    county = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.street} {self.town} {self.country}"


@receiver(post_save, sender=User)
def create_user_address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_address(sender, instance, **kwargs):
    instance.address.save()


class Feedback(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, blank=True)
    comments = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"{self.status} {self.comments}"
