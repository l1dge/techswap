from django.db import models


class Items(models.Model):
    itemID = models.IntegerField(primary_key=True, editable=False)
    PhotoID = models.ForeignKey("Photos", on_delete=models.CASCADE)
    ItemName = models.CharField(max_length=200)
    ItemCat = models.CharField(max_length=200)
    ItemCond = models.CharField(max_length=200)
    ItemLoc = models.CharField(max_length=200)
    SwapComp = models.BooleanField(default=False)
    ItemArch = models.BooleanField(default=False)
    ItemAct = models.BooleanField(default=False)
    SwapAgrd = models.BooleanField(default=False)


class Photos(models.Model):
    PhotoID = models.IntegerField(primary_key=True, editable=False)
    ItemID = models.ForeignKey(Items, on_delete=models.CASCADE)
    FileLoc = models.URLField()


class Categories(models.Model):
    CategoryID = models.IntegerField(primary_key=True, editable=False)
    ItemID = models.ForeignKey(Items, on_delete=models.CASCADE)
    CategoryName = models.CharField(max_length=200)
