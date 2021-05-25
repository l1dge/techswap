from django.db import models


class Wanted(models.Model):
    UserID = models.IntegerField(primary_key=True, editable=False)
    Location = models.CharField(max_length=200)
    ConditionReq = models.CharField(max_length=200)
    SwapAvail = models.BooleanField(default=False)
    ItemID = models.ForeignKey("itemmgmt.Items", on_delete=models.CASCADE)


class ForSwap(models.Model):
    UserID = models.IntegerField(primary_key=True, editable=False)
    ItemID = models.ForeignKey(
        "itemmgmt.Items", related_name="ItemID", on_delete=models.CASCADE
    )
    ItemCond = models.ForeignKey(
        "itemmgmt.Items",
        on_delete=models.CASCADE,
    )
    Location = models.CharField(max_length=200)
    SwapAvail = models.BooleanField(default=False)
