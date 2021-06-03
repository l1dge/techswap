from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Feedback(models.Model):
    status = models.CharField(max_length=200)
    comments = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.status} {self.comments}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(
        "usermgmt.Address",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    phone = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(default=0)
    feedback = models.ManyToManyField("Feedback", related_name="Feedback")

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
    house_num = models.IntegerField()
    street = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.street} {self.town} {self.country}"
