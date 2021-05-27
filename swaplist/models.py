from django.db import models


class Wanted(models.Model):
    UserID = models.ForeignKey(
        "usermgmt.Users",
        on_delete=models.CASCADE,
    )
    Location = models.CharField(max_length=200)
    ConditionReq = models.CharField(max_length=200)
    ItemID = models.ForeignKey("itemmgmt.Items", on_delete=models.CASCADE)


class ForSwap(models.Model):
    UserID = models.ForeignKey(
        "usermgmt.Users",
        on_delete=models.CASCADE,
    )
    ItemID = models.ForeignKey(
        "itemmgmt.Items", related_name="ItemID", on_delete=models.CASCADE
    )
    Location = models.ForeignKey(
        "itemmgmt.Location",
        on_delete=models.CASCADE,
    )
    SwapAvail = models.BooleanField(default=False)
