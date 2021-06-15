from django.contrib.auth.models import (
    User,
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.db.models.fields import TextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from location_field.models.plain import PlainLocationField
from django.utils.text import slugify
from django.utils.timezone import now
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Item Management
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


ITEM_CONDITION = (
    (s, s)
    for s in ("Like New", "Excelllent", "Good", "Used", "Poor", "Spares or Repair")
)


class Item(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default="", editable=False, max_length=255)
    category = models.ManyToManyField(Category)
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
    created_by = models.ForeignKey("AppUser", on_delete=models.DO_NOTHING)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {"pk": self.id, "slug": self.slug, "my_id": self.id}
        return reverse("itemdetail", kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.FileField(upload_to="items/multimages/")

    def __str__(self):
        return self.item.title


class Cart(models.Model):
    client = models.ForeignKey(
        "AppUser", on_delete=models.SET_NULL, null=True, blank=True
    )
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart: {self.id}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart: {self.cart.id} CartProduct: {self.id}"


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
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    swap_status = models.CharField(max_length=50, choices=SWAP_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    swap_completed = models.BooleanField(default=False, null=True, blank=True)

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


class Wanted(models.Model):
    user_id = models.ManyToManyField(
        "AppUser",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
    )
    condition_req = models.CharField(max_length=200)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} {self.location} {self.item_id}"


class ForSwap(models.Model):
    user_id = models.ManyToManyField(
        "AppUser",
    )
    item_id = models.ForeignKey(Item, related_name="ItemID", on_delete=models.CASCADE)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
    )
    swap_avail = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id} {self.location} {self.swap_avail}"


# User stuff
# class Admin(AbstractUser):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     image = models.FileField(upload_to="admins")
#     mobile = models.CharField(max_length=20)

#     def __str__(self):
#         return self.full_name


class CustomAccountManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        first_name,
        last_name,
        password,
        image,
        mobile,
        **other_fields,
    ):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            image=image,
            mobile=mobile,
            **other_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, username, first_name, last_name, password, **other_fields
    ):
        email = self.normalize_email(email)
        suser = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **other_fields,
        )
        suser.is_superuser = True
        suser.is_staff = True
        suser.is_active = True
        suser.set_password(password)
        suser.save()

        if not other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if not other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return suser


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), max_length=50, unique=True)
    username = models.CharField(unique=True, max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    image = models.FileField(upload_to="profile_images", null=True)
    mobile = models.CharField(max_length=20)
    joined_on = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "mobile",
    ]

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name} {self.mobile}"


class Profile(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True, blank=True)
    # image = models.FileField(upload_to="profile_images", default=None)
    rating = models.IntegerField(default=0)
    feedback = models.ManyToManyField("Feedback", related_name="Feedback")
    items = models.ManyToManyField(Item, related_name="Items")
    bio = models.TextField(_("bio"), max_length=500, blank=True)
    address = models.ForeignKey(
        "Address", on_delete=models.CASCADE, default=None, blank=True
    )
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
    house_num = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    town = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    county = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.street} {self.town} {self.country}"


class Feedback(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, blank=True)
    comments = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"{self.status} {self.comments}"
