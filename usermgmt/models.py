from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    profile = models.ForeignKey(
        "usermgmt.Profile",
        on_delete=models.CASCADE,
    )
    feedback = models.ManyToManyField("Feedback", related_name="Feedback")


class Feedback(models.Model):
    status = models.CharField(max_length=200)
    comments = models.TextField(max_length=300)


class Profile(models.Model):
    username = models.CharField(max_length=200)
    address = models.ForeignKey(
        "usermgmt.Address",
        on_delete=models.CASCADE,
    )
    email = models.CharField(max_length=200)
    email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=200)
    rating = models.IntegerField()


class Address(models.Model):
    house_num = models.IntegerField()
    street = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)
