from django.db import models


class Items(models.Model):
    ID = models.IntegerField(primary_key=True, editable=False)
    PhotoID = models.ForeignKey("Photos", on_delete=models.CASCADE)
    Feedback = models.ForeignKey(
        "usermgmt.Feedback", on_delete=models.CASCADE, default=None
    )
    Name = models.CharField(max_length=200)
    Category = models.ManyToManyField("Categories", related_name="Category")
    Condition = models.CharField(max_length=200)
    Location = models.CharField(max_length=200)
    SwapComp = models.BooleanField(default=False)
    Archived = models.BooleanField(default=False)
    Active = models.BooleanField(default=False)
    SwapAgrd = models.BooleanField(default=False)


class Photos(models.Model):
    ID = models.IntegerField(primary_key=True, editable=False)
    FileLoc = models.URLField()


class Categories(models.Model):
    ID = models.IntegerField(primary_key=True, editable=False)
    Name = models.CharField(max_length=200)


class Location(models.Model):
    ID = models.IntegerField(primary_key=True, editable=False)
    Name = models.CharField(max_length=200)
    Town = models.CharField(max_length=200)
    City = models.CharField(max_length=200)
    County = models.CharField(max_length=200)
    Country = models.CharField(max_length=200)
    Zip = models.CharField(max_length=200)
