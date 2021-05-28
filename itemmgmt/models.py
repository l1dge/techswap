from django.db import models


class Items(models.Model):
    photo_id = models.ForeignKey("photos", on_delete=models.CASCADE)
    feedback = models.ForeignKey(
        "usermgmt.Feedback", on_delete=models.CASCADE, default=None
    )
    name = models.CharField(max_length=200)
    category = models.ManyToManyField("categories", related_name="category")
    condition = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    swap_comp = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    swap_agrd = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s %s' % (self.name, self.category, self.location, self.active)


class Photos(models.Model):
    file_loc = models.URLField()

    def __str__(self):
        return '%s' % (self.file_loc)


class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % (self.name)


class Location(models.Model):
    name = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)

    def __str__(self):
        return '%s %s %s' % (self.name, self.town, self.country)
