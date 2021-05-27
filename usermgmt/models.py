from django.db import models


class Users(models.Model):
    Name = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)
    Profile = models.ForeignKey(
        "usermgmt.Profile",
        on_delete=models.CASCADE,
    )
    Feedback = models.ManyToManyField("Feedback", related_name="Feedback")


class Feedback(models.Model):
    Status = models.CharField(max_length=200)
    Comments = models.TextField(max_length=300)


class Profile(models.Model):
    Username = models.CharField(max_length=200)
    Address = models.ForeignKey(
        "usermgmt.Address",
        on_delete=models.CASCADE,
    )
    Email = models.CharField(max_length=200)
    EmailVerified = models.BooleanField(default=False)
    Phone = models.CharField(max_length=200)
    Rating = models.IntegerField()


class Address(models.Model):
    HouseNum = models.IntegerField()
    Street = models.CharField(max_length=200)
    Town = models.CharField(max_length=200)
    City = models.CharField(max_length=200)
    County = models.CharField(max_length=200)
    Country = models.CharField(max_length=200)
    Zip = models.CharField(max_length=200)
