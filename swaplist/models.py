from django.db import models
from django.contrib.auth.models import User


class Wanted(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    location = models.CharField(max_length=200)
    condition_req = models.CharField(max_length=200)
    item_id = models.ForeignKey("itemmgmt.Items", on_delete=models.CASCADE)


class ForSwap(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    item_id = models.ForeignKey(
        "itemmgmt.Items", related_name="ItemID", on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        "itemmgmt.Location",
        on_delete=models.CASCADE,
    )
    swap_avail = models.BooleanField(default=False)
